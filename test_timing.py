import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent / "src"))
from pdf_processor.cloud_vision import GeminiTimingExtractor

def main():
  # Point this to the page with the diagram (e.g., Page 6 or 20)
  # You need to have run the previous image generation step first!
  target_image = Path("src/pdf/ad7980_images/page_006.png")
  
  if not target_image.exists():
    print("Please run the image generation step first!")
    return

  try:
    # Ensure GEMINI_API_KEY is set in your terminal
    # export GEMINI_API_KEY="your_key_here"
    extractor = GeminiTimingExtractor()
    
    print(f"Analyzing {target_image}...")
    result = extractor.analyze_diagram(target_image)
    
    # Save the 'Gold Standard' timing spec
    output_path = Path("src/pdf/ad7980_timing_logic.json")
    with open(output_path, "w") as f:
      json.dump(result, f, indent=2)
      
    print(f"\nSuccess! Logic extracted to {output_path}")
    print(json.dumps(result, indent=2))
    
  except Exception as e:
    print(f"Failed: {e}")

if __name__ == "__main__":
  main()