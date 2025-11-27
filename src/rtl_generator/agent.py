import os
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage
from .tools import DatasheetNavigatorTool, DatasheetReaderTool

class RTLAgent:
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
    You are an expert FPGA RTL Design Agent. Your goal is to write production-quality SystemVerilog IP.
    
    PROTOCOL:
    1. Use 'list_datasheet_configurations' to understand supported modes.
    2. Identify the target configuration ID.
    3. Use 'read_technical_specs' to get EXACT timing constraints and pinouts.
    4. Generate the SystemVerilog code.
    
    STRICT NAMING CONVENTIONS:
    - **Inputs:** MUST end with `_i` (e.g., `clk_i`, `cnv_i`, `sdi_i`, `sdo_i`).
    - **Outputs:** MUST end with `_o` (e.g., `cnv_o`, `sck_o`, `busy_o`, `data_valid_o`).
    - **Resets:** Active Low Reset MUST be named `rstn_i`.
    - **Internals:** Do NOT use suffixes for internal wires/regs.
    
    ARCHITECTURAL PATTERN (Core + Wrapper):
    You must generate TWO modules in the output:
    1. **`module <name>_core`**: 
       - Contains the actual FSM, Datapath, and Timing Logic.
       - Pure logic, no I/O buffers (IBUF/OBUF).
       - All assertions (SVA) must be inside here.
    2. **`module <name>_wrapper`**:
       - The top-level module.
       - Instantiates the `_core`.
       - Maps top-level ports to core signals.
    
    CODING STANDARDS:
    - **Indentation:** STRICTLY 2 spaces.
    - **Logic:** Use `always_ff @(posedge clk_i or negedge rstn_i)` for sequential logic.
    - **FSM:** Use `unique case` for state transitions.
    - **Assertions:** Generate SVA inside the `_core` module using the specific timing values (t_CONV, etc) found in the context.
    """

    self.graph = create_react_agent(self.llm, self.tools)

  def run(self, user_query: str) -> str:
    print(f"--- RTL Agent Started: '{user_query}' ---")
    messages = [
      SystemMessage(content=self.system_prompt),
      HumanMessage(content=user_query)
    ]
    result = self.graph.invoke({"messages": messages})
    
    # FIX: Handle Gemini returning list-of-content blocks
    content = result["messages"][-1].content
    
    if isinstance(content, list):
      return "".join(block["text"] for block in content if "text" in block)
    
    return str(content)