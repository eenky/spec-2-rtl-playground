import typer
from pathlib import Path
from typing import Optional
import sys
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from pdf_processor import PDFProcessor, PDFExportConfig

app = typer.Typer(add_completion=False)

@app.command()
def main(
  input: Path = typer.Option(..., "--input", "-i", exists=True, dir_okay=False),
  output: Optional[Path] = typer.Option(None, "--output", "-o"),
  dpi: int = typer.Option(150, "--dpi")
):
  """Convert PDF to Images (Standard)."""
  print(f"--- Starting Processing: {input.name} ---")
  config = PDFExportConfig(dpi=dpi, image_format="png")
  try:
    with PDFProcessor(input) as processor:
      images = processor.convert_to_images(config, output_dir=output)
      print(f"Success! Generated {len(images)} images.")
  except Exception as e:
    print(f"Fatal Error: {e}")
    raise typer.Exit(code=1)

@app.command()
def ocr(
  input_dir: Path = typer.Option(..., "--input", "-i", exists=True, file_okay=False),
  output_dir: Path = typer.Option(..., "--output-dir", "-o"),
  extract_timing: bool = typer.Option(False, "--extract-timing", help="Enable Cloud Logic Extraction.")
):
  """
  Run OlmOCR on images. Smartly detects and extracts timing logic.
  """
  # 1. Setup Dependencies (New Imports)
  try:
    from ocr_engine import OlmOCRProcessor, GeminiTimingExtractor
    ocr_engine = OlmOCRProcessor()
  except ImportError as e:
    print(f"Error: Missing ML dependencies. {e}")
    raise typer.Exit(1)
    
  gemini_extractor = None
  if extract_timing:
    try:
      gemini_extractor = GeminiTimingExtractor()
      print("[INFO] Cloud Vision initialized.")
    except Exception as e:
      print(f"[WARN] Cloud Vision unavailable: {e}")
      extract_timing = False

  if not output_dir.exists():
    output_dir.mkdir(parents=True)

  images = sorted(list(input_dir.glob("*.png")))
  print(f"--- Processing {len(images)} pages ---")

  full_text_buffer = []

  for i, img in enumerate(images):
    print(f"[{i+1}/{len(images)}] Reading {img.name}...", end=" ", flush=True)
    
    try:
      # A. Local Text OCR
      page_text = ocr_engine.process_image(img)
      
      md_path = output_dir / f"{img.stem}.md"
      with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"\n\n{page_text}")
      
      full_text_buffer.append(f"\n\n\n{page_text}")
      print("Done.")

      # B. Diagram Detection Logic
      if extract_timing:
        keywords = ["timing", "switching", "waveform", "figure"]
        has_keyword = any(k in page_text.lower() for k in keywords)
        
        if has_keyword:
          print(f"      [?] Hints found. Verifying visual presence...", end=" ")
          if ocr_engine.has_visual_diagram(img):
            print("YES.")
            print(f"      [⚡] Sending to Gemini for Context Extraction...")
            try:
              logic_data = gemini_extractor.analyze_diagram(img)
              
              json_path = output_dir / f"{img.stem}_timing.json"
              with open(json_path, "w", encoding="utf-8") as f:
                json.dump(logic_data, f, indent=2)
                
              print(f"      [✓] Logic extracted: Mode='{logic_data.get('operating_mode', 'Unknown')}'")
            except Exception as e:
              print(f"      [X] Extraction failed: {e}")
          else:
            print("NO.")

    except Exception as e:
      print(f"\nError processing {img.name}: {e}")

  full_path = output_dir / "_full_datasheet.md"
  with open(full_path, "w", encoding="utf-8") as f:
    f.write("\n".join(full_text_buffer))
  print(f"\n--- Complete! Output in {output_dir} ---")

if __name__ == "__main__":
  app()