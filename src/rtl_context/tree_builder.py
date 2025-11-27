import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from .schema import KnowledgeNode

class KnowledgeTreeBuilder:
  def __init__(self, model_name: str = "gemini-2.5-flash"):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
      raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
      
    self.llm = ChatGoogleGenerativeAI(
      model=model_name,
      temperature=0,
      google_api_key=api_key,
      convert_system_message_to_human=True
    )

  def build_tree(self, flat_manifest: list) -> KnowledgeNode:
    """
    Constructs a hierarchical Knowledge Tree from a flat list of datasheet pages.
    """
    manifest_str = json.dumps(flat_manifest, indent=2)

    system_prompt = (
      "You are a Senior System Architect building an RTL generation context tree. "
      "Review the provided list of datasheet pages (metadata and summaries).\n\n"
      "Your Goal: Organize these pages into a Hierarchical Knowledge Tree (GROVE architecture) "
      "so an FPGA engineer can find information by traversing modes/features.\n\n"
      "Structure Rules:\n"
      "1. ROOT: The Device Name (e.g. AD7980).\n"
      "2. BRANCHES: Group by Operating Modes (e.g. '3-Wire CS Mode', 'Chain Mode') or major functional blocks.\n"
      "3. LEAVES: Specific constraints (Timing, Pinout, Registers).\n"
      "4. CRITICAL: Populate 'apply_condition' for EVERY node.\n\n"
      "You must output a SINGLE JSON object matching this EXACT schema:\n"
      "{{\n"
      "  \"id\": \"unique_string_id\",\n"
      "  \"type\": \"device_root\" | \"mode_group\" | \"sub_mode\" | \"leaf_fact\",\n"
      "  \"title\": \"Human Readable Title\",\n"
      "  \"description\": \"Summary of this node\",\n"
      "  \"apply_condition\": \"Logic condition (e.g. IF mode == SPI)\",\n"
      "  \"content_refs\": [ \"page_ids...\" ],\n"
      "  \"children\": [ ... recursive list of same objects ... ]\n"
      "}}\n"
    )

    prompt = ChatPromptTemplate.from_messages([
      ("system", system_prompt),
      ("human", "Here is the flat page manifest:\n{manifest}\n\nGenerate the Tree:")
    ])

    print(f"   [TreeBuilder] Architecting hierarchy with {self.llm.model}...")
    
    try:
      chain = prompt | self.llm
      response = chain.invoke({"manifest": manifest_str})
      
      # Robust Markdown Cleanup
      content = response.content.strip()
      if content.startswith("```json"):
        content = content[7:]
      elif content.startswith("```"):
        content = content[3:]
      
      if content.endswith("```"):
        content = content[:-3]
      
      content = content.strip()
      
      data = json.loads(content)
      return KnowledgeNode(**data)
      
    except Exception as e:
      print(f"   [TreeBuilder] Error: {e}")
      return None