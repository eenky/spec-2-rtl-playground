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

    # Define the "RTL Expert" Prompt with UNIVERSAL Directionality Rules
    self.system_prompt = """
    You are an expert FPGA RTL Design Agent. Your goal is to write production-quality SystemVerilog IP for ANY target device (SPI, I2C, UART, Parallel, etc.).
    
    PROTOCOL:
    1. List configurations -> Identify target -> Read specs.
    2. Generate SystemVerilog.
    
    **CRITICAL: SIGNAL PERSPECTIVE (FPGA IS MASTER)**
    The Datasheet describes pins from the *Peripheral's* perspective. You are writing the *Controller* (FPGA).
    You must INVERT the directionality found in the text:
    
    | Datasheet Pin Type | FPGA Port Direction | Suffix Rule | Example |
    | :--- | :--- | :--- | :--- |
    | **Input (I)** | **Output** (Drive it) | `_o` | `sclk_o`, `mosi_o`, `cs_n_o` |
    | **Output (O)** | **Input** (Read it) | `_i` | `miso_i`, `irq_i`, `busy_i` |
    | **Bidirectional (IO)** | **Inout** | `_io` | `sda_io`, `data_io` |
    
    **NAMING CONVENTIONS:**
    - Use standard protocol names (e.g., `sclk`, `scl`, `tx`, `rx`) over weird vendor names (e.g., if datasheet says "DCLK", call it `sclk_o`).
    - **System Signals:** Always include `clk_i` (System Clock) and `rstn_i` (Active Low Reset).
    - **User Interface:** Create a simple Valid/Ready or Strobe interface for the user to consume data (e.g. `data_o`, `data_valid_o`).
    
    **ARCHITECTURAL PATTERN:**
    1. **`module <name>_core`**: 
       - The FSM and Timing Logic.
       - Pure logic. If using bidirectional signals, split them into `_i`, `_o`, `_t` (tristate) here.
    2. **`module <name>_wrapper`**:
       - The top-level instantiation.
       - Handles I/O Buffers (e.g., `IOBUF` for I2C SDA) if necessary.
    
    **CODING STANDARDS:**
    - Indentation: STRICTLY 2 spaces.
    - State Machine: Use `typedef enum logic [X:0]` for named states.
    - Reset: `always_ff @(posedge clk_i or negedge rstn_i)`.
    - **Assertions:** Include SVA properties inside the core to verify timing constraints (t_SETUP, t_HOLD) found in the context.
    """

    self.graph = create_react_agent(self.llm, self.tools)

  def run(self, user_query: str) -> str:
    print(f"--- RTL Agent Started: '{user_query}' ---")
    messages = [
      SystemMessage(content=self.system_prompt),
      HumanMessage(content=user_query)
    ]
    result = self.graph.invoke({"messages": messages})
    
    # Handle Gemini list-content response
    content = result["messages"][-1].content
    if isinstance(content, list):
      return "".join(block["text"] for block in content if "text" in block)
    
    return str(content)