import sys
from pathlib import Path

# 1. Add 'src' to the python path so we can import our new package
#    (This mimics how it works when installed as a real package)
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pdf_processor import PDFProcessor, PDFExportConfig

def main():
  print("--- Starting Manual Test ---")

  # Define our inputs
  # We assume the script is running from spec-2-rtl-playground/
  pdf_path = Path("src/pdf/ad7980.pdf")
  
  if not pdf_path.exists():
    print(f"Error: Cannot find test file at {pdf_path}")
    return

  # Create a configuration (Let's try 200 DPI for higher quality)
  config = PDFExportConfig(dpi=200, image_format="png")

  # Run the processor using the Context Manager
  try:
    with PDFProcessor(pdf_path) as processor:
      images = processor.convert_to_images(config)
      
      print("\n--- Test Results ---")
      print(f"Generated {len(images)} images in: {processor.default_output_dir}")
      print("Check that folder to see if the images look correct.")

  except Exception as e:
    print(f"Test Failed with error: {e}")

if __name__ == "__main__":
  main()