import os
import json
import google.generativeai as genai
from pathlib import Path
from typing import Optional, Dict, Any
from .utils import setup_logger

class GeminiTimingExtractor:
  def __init__(self, api_key: Optional[str] = None):
    self.logger = setup_logger("GeminiVision")
    
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
      raise ValueError("GEMINI_API_KEY not found. Please set it in your environment.")
      
    genai.configure(api_key=key)
    
    # UPDATE: Use the 2.5 Pro Stable endpoint
    # This model has the "Thinking" capability enabled by default for complex tasks.
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
    
    Goal: We need to write a SystemVerilog Assertion (SVA) based on this image.
    
    Output JSON with these specific keys:
    1. "clock_domain": Identify the main clock signal (e.g., SCK) and its active edge (Rising/Falling).
    2. "causality": A list of objects describing triggers. 
       Format: {"trigger": "CNV Rising", "effect": "SDO High-Z", "delay": "t_dis"}
    3. "constraints": Key-Value pairs of all labeled timing parameters (e.g., {"t_conv": "Conversion Time", "t_acq": "Acquisition Time"}).
    4. "bus_states": Describe the state of data buses (e.g., "SDO is High-Z until the first falling edge of SCK").
    
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