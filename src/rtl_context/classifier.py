from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from .schema import PageAnalysis, PageType

class PageClassifier:
  # UPDATED: Defaults to the Qwen3 14B model you pulled
  def __init__(self, model_name: str = "qwen3:14b"):
    self.llm = ChatOllama(model=model_name, temperature=0, format="json")
    self.parser = PydanticOutputParser(pydantic_object=PageAnalysis)
    
    system_prompt = (
      "You are a Senior FPGA Verification Engineer. "
      "Your job is to analyze datasheet pages and filter them for RTL development.\n"
      "Ignore marketing fluff, mechanical drawings, and ordering guides.\n"
      "Focus strictly on Timing, Pinouts, Logic Protocols, and State Machines.\n\n"
      "You must respond with valid JSON matching the following schema:\n"
      "{format_instructions}"
    )
    
    self.prompt = ChatPromptTemplate.from_messages([
      ("system", system_prompt),
      ("human", "Page ID: {page_id}\n\nContent Snippet:\n{page_content}")
    ])
    
    self.chain = self.prompt | self.llm | self.parser

  def analyze_page(self, page_id: str, content: str) -> PageAnalysis:
    # Qwen3 has a large context window, so we can be generous
    safe_content = content[:12000]
    
    try:
      return self.chain.invoke({
        "page_id": page_id,
        "page_content": safe_content,
        "format_instructions": self.parser.get_format_instructions()
      })
    except Exception as e:
      print(f"   [X] Classification error on {page_id}: {e}")
      return PageAnalysis(
        page_id=page_id,
        page_type=PageType.IRRELEVANT,
        relevance_score=0,
        summary="Classification Failed",
        key_signals=[]
      )