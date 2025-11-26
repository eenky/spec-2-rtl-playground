import torch
from pathlib import Path
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
from .utils import setup_logger

class OlmOCRProcessor:
  def __init__(self):
    self.logger = setup_logger("OlmOCR-2")
    self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # 1. Configuration for OlmOCR 2 (Qwen2.5-VL based)
    # We use the official model for weights, but the base model for the processor
    # to guarantee we get the correct image resizing logic and chat templates.
    self.model_id = "allenai/olmOCR-2-7B-1025"
    self.base_model_id = "Qwen/Qwen2.5-VL-7B-Instruct" 

    self.logger.info(f"Initializing {self.model_id} on {self.device}...")

    # 2. Load Processor
    try:
      self.processor = AutoProcessor.from_pretrained(self.base_model_id)
    except Exception:
      self.logger.warning("Could not load base processor. Falling back to model ID.")
      self.processor = AutoProcessor.from_pretrained(self.model_id)

    # 3. Determine Attention Backend
    try:
      import flash_attn
      attn_impl = "flash_attention_2"
      self.logger.info("Using Flash Attention 2 ⚡")
    except ImportError:
      attn_impl = "sdpa" 
      self.logger.info("Using PyTorch SDPA (Standard Attention).")

    # 4. Load Model
    # Qwen2.5-VL requires 'AutoModelForVision2Seq'
    self.model = AutoModelForVision2Seq.from_pretrained(
      self.model_id,
      torch_dtype=torch.bfloat16,  # Native precision for 3090 Ti
      attn_implementation=attn_impl,
      device_map="auto"
    )
    
    self.logger.info(f"Model loaded. VRAM usage: {torch.cuda.memory_allocated()/1024**3:.2f} GB")

  def process_image(self, image_path: Path) -> str:
    """
    Runs OlmOCR 2 on a single image.
    """
    if not image_path.exists():
      raise FileNotFoundError(f"Image not found: {image_path}")

    self.logger.debug(f"Processing image: {image_path.name}")
    
    image = Image.open(image_path).convert("RGB")
    
    # 5. The "No-Anchor" Prompt
    # OlmOCR 2 is fine-tuned to act as a transcriber. 
    # We explicitly tell it NOT to look for anchors (since we don't have them).
    prompt_text = (
      "Accurately transcribe the text, tables, and layout of this document image into Markdown. "
      "Use LaTeX for equations. Represent tables using standard Markdown syntax. "
      "Do not output any conversational text, just the document content."
    )

    messages = [
      {
        "role": "user",
        "content": [
          {"type": "image", "image": image},
          {"type": "text", "text": prompt_text}
        ]
      }
    ]

    # Preprocess inputs
    text = self.processor.apply_chat_template(
      messages, tokenize=False, add_generation_prompt=True
    )
    
    # Qwen2.5-VL image processing
    inputs = self.processor(
      images=[image],
      text=[text],
      padding=True,
      return_tensors="pt"
    ).to(self.device)

    # Generate
    with torch.no_grad():
      generated_ids = self.model.generate(
        **inputs,
        max_new_tokens=4096,  # OlmOCR 2 supports very long context
        temperature=0.1,      # Low temp for precision
        do_sample=True,
        use_cache=True
      )
    
    # Trim inputs from outputs
    generated_ids_trimmed = [
      out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    
    output_text = self.processor.batch_decode(
      generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )[0]
    
    return output_text