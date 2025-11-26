import sys
from pathlib import Path
import json
import os

sys.path.insert(0, str(Path(__file__).parent / "src"))
from ocr_engine import GeminiTimingExtractor

def main():
  # We target Page 20 explicitly to test "Operating Mode" detection
  # (Make sure you generated images first!)
  target_image = Path("src/pdf/ad7980_images/page_020.png")
  
  if not target_image.exists():
    print(f"Error: {target_image} does not exist. Run the image converter first.")
    return

  try:
    print(f"--- Testing Gemini 2.5 Pro on {target_image.name} ---")
    extractor = GeminiTimingExtractor()
    
    result = extractor.analyze_diagram(target_image)
    
    output_path = Path("src/pdf/ad7980_page_20_timing.json")
    with open(output_path, "w") as f:
      json.dump(result, f, indent=2)
      
    print(f"\n[SUCCESS] Mode Detected: {result.get('operating_mode')}")
    print(f"Logic saved to {output_path}")
    
  except Exception as e:
    print(f"Failed: {e}")

if __name__ == "__main__":
  main()