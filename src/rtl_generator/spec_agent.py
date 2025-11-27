import os
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage
from .tools import DatasheetNavigatorTool, DatasheetReaderTool

class SpecGenAgent:
  def __init__(self, context_dir: Path, md_dir: Path, model_name: str = "gemini-2.5-flash"):
    self.tree_path = context_dir / "rtl_knowledge_tree.json"
    if not self.tree_path.exists():
      raise FileNotFoundError(f"Tree not found at {self.tree_path}")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
      raise ValueError("GEMINI_API_KEY not found.")

    self.llm = ChatGoogleGenerativeAI(
      model=model_name,
      temperature=0,
      google_api_key=api_key
    )

    self.tools = [
      DatasheetNavigatorTool(tree_path=self.tree_path),
      DatasheetReaderTool(tree_path=self.tree_path, md_dir=md_dir)
    ]

    self.system_prompt = """
    You are a Senior Systems Engineer creating a Hardware Requirements Specification (HRS).
    
    PROTOCOL:
    1. Find the user's requested mode via 'list_datasheet_configurations'.
    2. Retrieve constraints via 'read_technical_specs'.
    3. Draft the Spec.
    
    STRICT PINOUT RULES:
    - **External Interface (PHY):** You must ONLY list pins found in the Datasheet 'Pin Configuration' section. DO NOT invent a Reset pin if the chip does not have one.
    - **System Interface (User):** You MAY add standard FPGA control signals (`clk_i`, `rstn_i`, `start_i`, `data_valid_o`) required to drive the internal state machine, but clearly label them as "FPGA System Signals".
    
    NAMING CONVENTION (STRICT):
    - Inputs: `_i` suffix (e.g. `sdo_i`, `clk_i`).
    - Outputs: `_o` suffix (e.g. `cnv_o`, `sck_o`).
    - Active Low Reset: Must be named `rstn_i`.
    
    OUTPUT FORMAT (Markdown):
    
    # Hardware Requirements: [Mode Name]
    
    ## 1. Interface Definition
    ### 1.1 External Device Interface (PHY)
    (List ONLY pins physically present on the chip. Source: Pinout Table)
    ### 1.2 FPGA System Interface (User Side)
    (List clk_i, rstn_i, and data_o valid/ready handshaking signals)
    
    ## 2. Timing Constraints (REQT-TMG-xxx)
    (Use specific nanosecond values from the text. e.g. "t_CONV max 710ns")
    
    ## 3. Functional Logic (REQT-LOG-xxx)
    (State machine behavior, Busy Indicator handling, etc.)
    
    ## 4. Architecture Strategy
    (Describe the _core / _wrapper separation. The _core handles the FSM, the _wrapper handles instantiation.)
    """

    self.graph = create_react_agent(self.llm, self.tools)

  def run(self, user_query: str) -> str:
    print(f"--- Spec Agent Started: '{user_query}' ---")
    messages = [
      SystemMessage(content=self.system_prompt),
      HumanMessage(content=user_query)
    ]
    result = self.graph.invoke({"messages": messages})
    
    # FIX: Handle Gemini returning list-of-content blocks
    content = result["messages"][-1].content
    
    if isinstance(content, list):
      # Join text blocks if it's a list
      return "".join(block["text"] for block in content if "text" in block)
    
    return str(content)