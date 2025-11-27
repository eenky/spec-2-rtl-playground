import json
from pathlib import Path
from typing import Optional, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from rtl_context import TreeNavigator

# --- Input Schemas ---

class LookupOptionsInput(BaseModel):
  query: str = Field(description="Optional search term to filter configurations (e.g. '3-wire').")

class ReadSpecsInput(BaseModel):
  config_id: str = Field(..., description="The ID of the configuration to retrieve (e.g. '3wire_busy').")

# --- Tool Definitions ---

class DatasheetNavigatorTool(BaseTool):
  # FIX: Added type annotations for Pydantic v2
  name: str = "list_datasheet_configurations"
  description: str = "Lists all available hardware operating modes and configurations found in the datasheet tree."
  args_schema: Type[BaseModel] = LookupOptionsInput
  tree_path: Path

  def _run(self, query: str = "") -> str:
    nav = TreeNavigator(self.tree_path)
    options = nav.list_configurations()
    
    # Smart Filtering Logic
    filtered_options = []
    query = query.lower().strip()
    
    # 1. Check if query matches the Root Device (e.g. "AD7980")
    # If the user asks for the device name, they want to see everything.
    device_name = nav.root.title.lower()
    if query in device_name or query == "":
      filtered_options = options
    else:
      # 2. Otherwise filter by specific mode name
      for opt in options:
        if query in opt['name'].lower() or query in opt['id'].lower():
          filtered_options.append(opt)
    
    # 3. Fallback: If filter killed everything, return ALL options (Better than empty)
    if not filtered_options:
      output = f"No exact matches for '{query}'. Showing ALL available configurations:\n\n"
      filtered_options = options
    else:
      output = f"Available Configurations matching '{query}':\n\n"

    # Format Output
    for opt in filtered_options:
      output += f"- Name: {opt['name']}\n"
      output += f"  ID: {opt['id']}\n"
      output += f"  Logic: {opt['description']}\n"
      output += f"  Condition: {opt['condition']}\n"
      output += "--------------------------------------------------\n"
      
    return output

class DatasheetReaderTool(BaseTool):
  name: str = "read_technical_specs"
  description: str = "Retrieves the specific Timing Constraints, Pinouts, and Logic diagrams for a specific Configuration ID."
  args_schema: Type[BaseModel] = ReadSpecsInput
  tree_path: Path
  md_dir: Path

  def _run(self, config_id: str) -> str:
    nav = TreeNavigator(self.tree_path)
    context = nav.get_node_context(config_id)
    
    if "error" in context:
      return f"Error: {context['error']}"

    full_content = f"--- CONTEXT FOR CONFIGURATION: {context['config_name']} ---\n"
    full_content += f"Apply Condition: {context['apply_condition']}\n\n"
    
    # Debug: Print what we are retrieving
    # print(f"[Tool] Retrieving pages: {context['relevant_pages']}")

    for page_file in context['relevant_pages']:
      # Check for Timing JSON first (High Precision)
      json_path = self.md_dir / f"{page_file}_timing.json"
      if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
          full_content += f"\n--- LOGIC/TIMING ({page_file}) ---\n"
          full_content += f.read()
          full_content += "\n---------------------------------\n"
      
      # Check for Markdown (Text/Pinout)
      md_path = self.md_dir / f"{page_file}.md"
      if md_path.exists():
        with open(md_path, "r") as f:
          full_content += f"\n--- TEXT DOCS ({page_file}) ---\n"
          full_content += f.read()
          full_content += "\n---------------------------------\n"

    return full_content