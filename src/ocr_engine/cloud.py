import os
import json
import google.generativeai as genai
from pathlib import Path
from typing import Optional, Dict, Any
from pdf_processor.utils import setup_logger

class GeminiTimingExtractor:
  def __init__(self, api_key: Optional[str] = None):
    self.logger = setup_logger("GeminiVision")
    
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
      raise ValueError("GEMINI_API_KEY not found. Please set it in your environment.")
      
    genai.configure(api_key=key)
    
    # Use the 2.5 Pro Stable endpoint
    self.model_name = 'gemini-2.5-pro'
    
    self.model = genai.GenerativeModel(self.model_name)
    self.logger.info(f"Initialized {self.model_name} for Timing Analysis")

  def analyze_diagram(self, image_path: Path) -> Dict[str, Any]:
    """
    Extracts timing logic from a datasheet crop.
    """
    if not image_path.exists():
      raise FileNotFoundError(f"Image not found: {image_path}")
      
    self.logger.info(f"Uploading {image_path.name} to Gemini...")
    
    sample_file = genai.upload_file(path=str(image_path), display_name=image_path.name)
    
    # Verification Prompt
    prompt = """
    Role: Senior FPGA Verification Engineer.
    Task: Extract the formal timing constraints and logic causality from this diagram.
    
    CRITICAL STEP: Look at the Page Headers, Section Titles, and Figure Captions to determine the "Operating Mode".
    (Examples: "3-Wire CS Mode", "Chain Mode", "With Busy Indicator", "No Busy Indicator").
    
    Output a JSON object with this specific structure:
    {
      "operating_mode": "The specific mode name found",
      "clock_domain": { 
        "signal": "Name of clock", 
        "active_edge": "Rising/Falling" 
      },
      "causality": [
        {"trigger": "CNV Rising", "effect": "SDO High-Z", "delay": "t_dis"}
      ],
      "constraints": {"t_conv": "Conversion Time", "t_acq": "Acquisition Time"},
      "bus_states": "Description of High-Z states or data validity windows.",
      "notes": "Any special constraints mentioned in footnotes."
    }
    
    Warning: Be precise about "High-Z" (High Impedance) states shown by dashed lines.
    """
    
    try:
      self.logger.info("Thinking...")
      response = self.model.generate_content([sample_file, prompt])
      
      text = response.text.strip()
      if text.startswith("```json"):
        text = text[7:-3].strip()
      
      return json.loads(text)
      
    except Exception as e:
      self.logger.error(f"Cloud analysis failed: {e}")
      return {"error": str(e)}
      
    finally:
      sample_file.delete()