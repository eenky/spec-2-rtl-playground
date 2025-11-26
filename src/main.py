import typer
from pathlib import Path
from typing_extensions import Annotated
from tqdm import tqdm # Progress bar

# Import our custom modules
from pdf_processor import PDFProcessor
from ocr_engine import OCREngine

app = typer.Typer()

@app.command()
def process(
  input_path: Annotated[Path, typer.Option("--input", help="Path to input PDF OR a folder of images", exists=True)],
  output_markdown: Annotated[Path, typer.Option("--output", help="Path to the output markdown file")] = Path("output.md")
):
  """   
  Can accept a PDF (converts to images first) or a Folder (processes images directly).
  """
  
  # 1. Determine Input Type
  image_paths = []
  working_dir = None

  if input_path.is_file() and input_path.suffix.lower() == ".pdf":
  # It's a PDF. Convert it.
  working_dir = input_path.parent / input_path.stem
  processor = PDFProcessor(zoom_factor=2)
  image_paths = processor.convert_to_images(input_path, working_dir)
  
  elif input_path.is_dir():
  # It's a folder. Look for images.
  working_dir = input_path
  valid_exts = {".jpg", ".jpeg", ".png", ".bmp"}
  image_paths = sorted([
    p for p in input_path.iterdir() 
    if p.is_file() and p.suffix.lower() in valid_exts
  ])
  if not image_paths:
    print(f"No images found in {input_path}")
    return
  else:
  print("Input must be a PDF file or a directory of images.")
  return

  # 2. Initialize Engine (Load Model)
  try:
  engine = OCREngine()
  except Exception as e:
  print(f"Failed to load model: {e}")
  return

  # 3. Run Inference Loop
  full_markdown_content = []
  
  print(f"Starting OCR on {len(image_paths)} images...")
  
  # tqdm creates a nice progress bar in the terminal
  for i, img_path in enumerate(tqdm(image_paths, unit="page")):
  try:
    # We pass working_dir to allow the model to save debug artifacts if configured
    page_content = engine.process_image(img_path, working_dir)
    
    # Add headers
    full_markdown_content.append(f"## Page {i+1} ({img_path.name})\n\n{page_content}")
  except Exception as e:
    print(f"\nError processing {img_path.name}: {e}")
    full_markdown_content.append(f"## Page {i+1} (Error)\n\n[OCR Failed: {e}]")

  # 4. Save Output
  with open(output_markdown, "w", encoding="utf-8") as f:
  f.write("\n\n".join(full_markdown_content))

  print(f"\nSuccess! Output saved to: {output_markdown}")

if __name__ == "__main__":
  app()