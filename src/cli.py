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
  output_dir: Path = typer.Option(
    ..., 
    "--output-dir", "-o", 
    help="Directory to save individual markdown files."
  ),
  save_full: bool = typer.Option(
    True, 
    "--save-full/--no-save-full", 
    help="Also save a combined _full.md file for easy reading."
  )
):
  """
  Run OlmOCR on a folder of images, saving individual markdown files.
  """
  try:
    from pdf_processor.ocr import OlmOCRProcessor
  except ImportError as e:
    print(f"Error: Missing ML dependencies. {e}")
    raise typer.Exit(1)
  
  # 1. Setup Output Directory
  if not output_dir.exists():
    output_dir.mkdir(parents=True)
    print(f"Created output directory: {output_dir}")

  print(f"--- Starting OCR on folder: {input_dir} ---")
  
  # 2. Initialize Engine
  try:
    ocr_engine = OlmOCRProcessor()
  except Exception as e:
    print(f"Failed to load OCR engine: {e}")
    raise typer.Exit(1)

  # 3. Gather Images
  images = sorted(list(input_dir.glob("*.png")))
  if not images:
    print("No .png files found.")
    raise typer.Exit(1)

  print(f"Found {len(images)} images. Processing...")

  full_text_buffer = []

  # 4. Process Loop
  import time
  start_time = time.time()

  for i, img in enumerate(images):
    print(f"[{i+1}/{len(images)}] Reading {img.name}...")
    try:
      # Run Model
      page_text = ocr_engine.process_image(img)
      
      # A. Save Individual File (e.g., page_001.md)
      md_filename = f"{img.stem}.md"
      md_path = output_dir / md_filename
      
      with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"\n\n")
        f.write(page_text)
      
      # B. Buffer for full file
      if save_full:
        full_text_buffer.append(f"\n\n\n{page_text}")
        
    except Exception as e:
      print(f"Error reading {img.name}: {e}")

  # 5. Save Full (Optional)
  if save_full and full_text_buffer:
    full_path = output_dir / "_full_datasheet.md"
    with open(full_path, "w", encoding="utf-8") as f:
      f.write("\n".join(full_text_buffer))
    print(f"Saved combined file to: {full_path}")
  
  elapsed = time.time() - start_time
  print(f"--- Complete! Processed {len(images)} pages in {elapsed:.1f}s ---")

if __name__ == "__main__":
  app()