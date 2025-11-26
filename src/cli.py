import typer
from pathlib import Path
from typing import Optional
import sys

# Add src to path so we can import our package
sys.path.insert(0, str(Path(__file__).parent))

from pdf_processor import PDFProcessor, PDFExportConfig

# Create the application
app = typer.Typer(add_completion=False)

@app.command()
def main(
  input: Path = typer.Option(
    ..., 
    "--input", "-i", 
    help="Path to the source PDF file.", 
    exists=True, 
    dir_okay=False
  ),
  output: Optional[Path] = typer.Option(
    None, 
    "--output", "-o", 
    help="Custom output directory."
  ),
  dpi: int = typer.Option(
    150, 
    "--dpi", 
    help="Resolution for the output images."
  )
):
  """
  Convert a PDF file into a sequence of images.
  """
  
  # Typer handles the "input exists" check automatically with exists=True above!
  
  print(f"--- Starting Processing: {input.name} ---")

  config = PDFExportConfig(dpi=dpi, image_format="png")

  try:
    with PDFProcessor(input) as processor:
      # We pass the output path (even if None) and let core handle the default logic
      images = processor.convert_to_images(config, output_dir=output)
      
      print(f"Success! Generated {len(images)} images.")
      
  except Exception as e:
    print(f"Fatal Error: {e}")
    raise typer.Exit(code=1)

@app.command()
def ocr(
  input_dir: Path = typer.Option(
    ..., 
    "--input", "-i", 
    help="Directory containing images to process.", 
    exists=True, 
    file_okay=False
  ),
  output: Path = typer.Option(
    "output.md", 
    "--output", "-o", 
    help="Path to save the combined markdown file."
  )
):
  """
  Run OlmOCR on a folder of images.
  """
  # We import inside the function so the rest of the CLI works 
  # even if dependencies (torch/transformers) are missing.
  try:
    from pdf_processor.ocr import OlmOCRProcessor
  except ImportError as e:
    print(f"Error: Missing ML dependencies. Please run 'uv add torch transformers accelerate pillow'")
    print(f"Details: {e}")
    raise typer.Exit(1)
  
  print(f"--- Starting OCR on folder: {input_dir} ---")
  
  # 1. Initialize Engine
  try:
    ocr_engine = OlmOCRProcessor()
  except Exception as e:
    print(f"Failed to load OCR engine: {e}")
    raise typer.Exit(1)

  # 2. Gather Images (Naturally sorted)
  images = sorted(list(input_dir.glob("*.png")))
  
  if not images:
    print("No .png files found in input directory.")
    raise typer.Exit(1)

  print(f"Found {len(images)} images. Processing sequentially...")

  full_text = []

  # 3. Process Loop
  import time
  start_time = time.time()

  for i, img in enumerate(images):
    print(f"[{i+1}/{len(images)}] Reading {img.name}...")
    try:
      page_text = ocr_engine.process_image(img)
      
      # Add page delimiter and content
      page_section = f"\n\n\n# Page: {img.stem}\n\n{page_text}"
      full_text.append(page_section)
      
    except Exception as e:
      print(f"Error reading {img.name}: {e}")

  # 4. Save
  with open(output, "w", encoding="utf-8") as f:
    f.write("\n".join(full_text))
  
  elapsed = time.time() - start_time
  print(f"--- Complete! Processed {len(images)} pages in {elapsed:.1f}s ---")
  print(f"Saved to: {output}")    

if __name__ == "__main__":
  app()