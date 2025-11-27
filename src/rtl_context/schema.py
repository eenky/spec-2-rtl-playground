from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

# --- Page Definitions ---
class PageType(str, Enum):
  TIMING_SPEC = "timing_spec"
  PINOUT = "pinout"
  PROTOCOL = "protocol"
  REGISTER_MAP = "register_map"
  BLOCK_DIAGRAM = "block_diagram"
  ELECTRICAL = "electrical"
  MECHANICAL = "mechanical"
  MARKETING = "marketing"
  IRRELEVANT = "irrelevant"

class PageAnalysis(BaseModel):
  """Structured analysis of a single datasheet page."""
  page_id: str = Field(..., description="The filename (e.g. page_006)")
  page_type: PageType
  relevance_score: int = Field(..., description="Score 0-10 for RTL utility.")
  summary: str
  key_signals: List[str]

# --- Tree Definitions ---
class NodeType(str, Enum):
  ROOT = "device_root"
  MODE_GROUP = "mode_group"
  SUB_MODE = "sub_mode"
  LEAF_FACT = "leaf_fact"

class KnowledgeNode(BaseModel):
  """Node in the GROVE Knowledge Tree."""
  id: str
  type: NodeType
  title: str
  description: str
  apply_condition: str = Field(..., description="Logic condition for when to use this node.")
  
  # Validated fix: Use simple strings for references to avoid schema complexity
  content_refs: List[str] = Field(default_factory=list)
  
  children: List['KnowledgeNode'] = Field(default_factory=list)

# Required for recursive Pydantic models
KnowledgeNode.update_forward_refs()