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

if __name__ == "__main__":
  app()