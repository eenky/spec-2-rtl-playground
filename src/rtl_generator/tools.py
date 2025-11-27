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
  # FIX: Add type annotations for Pydantic v2 compliance
  name: str = "list_datasheet_configurations"
  description: str = "Lists all available hardware operating modes and configurations found in the datasheet tree."
  args_schema: Type[BaseModel] = LookupOptionsInput
  
  # Custom fields need annotations too
  tree_path: Path

  def _run(self, query: str = "") -> str:
    nav = TreeNavigator(self.tree_path)
    options = nav.list_configurations()
    
    output = "Available Configurations:\n"
    for opt in options:
      if query.lower() in opt['name'].lower() or query == "":
        output += f"- Name: {opt['name']}\n  ID: {opt['id']}\n  Logic: {opt['description']}\n  Condition: {opt['condition']}\n\n"
    return output

class DatasheetReaderTool(BaseTool):
  # FIX: Add type annotations here too
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
    
    for page_file in context['relevant_pages']:
      # Check for Timing JSON first
      json_path = self.md_dir / f"{page_file}_timing.json"
      if json_path.exists():
        with open(json_path, "r") as f:
          full_content += f"\n--- LOGIC/TIMING ({page_file}) ---\n"
          full_content += f.read()
          full_content += "\n---------------------------------\n"
      
      # Check for Markdown
      md_path = self.md_dir / f"{page_file}.md"
      if md_path.exists():
        with open(md_path, "r") as f:
          full_content += f"\n--- TEXT DOCS ({page_file}) ---\n"
          full_content += f.read()
          full_content += "\n---------------------------------\n"

    return full_content