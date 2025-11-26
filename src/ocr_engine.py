import os
import torch
from pathlib import Path
from transformers import AutoModel, AutoTokenizer

# Enforce CUDA device
os.environ["CUDA_VISIBLE_DEVICES"] = '0'

class OCREngine:
  def __init__(self, model_name: str = 'deepseek-ai/DeepSeek-OCR'):
    print(f"[OCR] Loading {model_name} with bfloat16...")
    
    self.tokenizer = AutoTokenizer.from_pretrained(
      model_name, 
      trust_remote_code=True
    )
    
    # Load model the official way - NO quantization
    self.model = AutoModel.from_pretrained(
      model_name, 
      trust_remote_code=True, 
      use_safetensors=True,
      torch_dtype=torch.bfloat16,
      device_map="auto"
    )
    
    self.model = self.model.eval()
    
    self.prompt = "<image>\n<|grounding|>Convert the document to markdown. "

  def process_image(self, image_path: Path, output_dir: Path) -> str:
    """
    Runs inference on a single image.
    """
    res = self.model.infer(
      self.tokenizer, 
      prompt=self.prompt, 
      image_file=str(image_path), 
      output_path=str(output_dir),
      base_size=1024, 
      image_size=640, 
      crop_mode=True, 
      save_results=False, 
      test_compress=True
    )
    return res