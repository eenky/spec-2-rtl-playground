import json
from pathlib import Path
from typing import List, Dict, Optional, Set, Any
from .schema import KnowledgeNode, NodeType

class TreeNavigator:
  def __init__(self, tree_path: Path):
    if not tree_path.exists():
      raise FileNotFoundError(f"Context tree not found at {tree_path}")
      
    with open(tree_path, "r", encoding="utf-8") as f:
      data = json.load(f)
      # Load the root node (triggers recursive Pydantic validation)
      self.root = KnowledgeNode(**data)

  def list_configurations(self) -> List[Dict[str, str]]:
    """
    Deterministic walker. Finds all 'Sub-Mode' nodes which represent 
    selectable hardware configurations.
    """
    configs = []
    
    def _walk(node: KnowledgeNode, path_name: str):
      # Base Case: We found a selectable configuration mode
      if node.type == NodeType.SUB_MODE:
        full_name = f"{path_name} > {node.title}" if path_name else node.title
        configs.append({
          "id": node.id,
          "name": full_name,
          "description": node.description,
          "condition": node.apply_condition
        })
      
      # Recursive Step
      for child in node.children:
        # Only traverse structural nodes (Groups/Modes), ignore leaf facts for the menu
        if child.type in [NodeType.MODE_GROUP, NodeType.SUB_MODE]:
          # Build the breadcrumb path (e.g. "Serial Interface")
          current_path = node.title if node.type != NodeType.ROOT else ""
          if path_name:
            current_path = f"{path_name} > {node.title}"
            
          _walk(child, current_path)
        elif child.type == NodeType.ROOT:
           _walk(child, "")

    _walk(self.root, "")
    return configs

  def get_node_context(self, target_node_id: str) -> Dict[str, Any]:
    """
    The 'Zoom' function. Given a specific mode ID (e.g. '3wire_busy'),
    it collects ALL relevant constraints from that node AND its parents.
    """
    target_node = self._find_node_recursive(self.root, target_node_id)
    if not target_node:
      return {"error": f"Node {target_node_id} not found"}

    relevant_pages = set()
    
    # A. Target Node Content
    self._collect_leaf_content(target_node, relevant_pages)
    
    # B. Global Content (Heuristic: Direct children of Root that are LEAF_FACTs)
    for child in self.root.children:
      if child.type == NodeType.LEAF_FACT:
        relevant_pages.update(child.content_refs)
      if child.title.lower().startswith("global"):
        self._collect_leaf_content(child, relevant_pages)

    return {
      "config_id": target_node.id,
      "config_name": target_node.title,
      "apply_condition": target_node.apply_condition,
      "relevant_pages": sorted(list(relevant_pages))
    }

  def _find_node_recursive(self, current: KnowledgeNode, target_id: str) -> Optional[KnowledgeNode]:
    if current.id == target_id:
      return current
    for child in current.children:
      found = self._find_node_recursive(child, target_id)
      if found: return found
    return None

  def _collect_leaf_content(self, node: KnowledgeNode, refs: Set[str]):
    """Helper to gather content_refs from a node and all its leaf children."""
    if node.content_refs:
      refs.update(node.content_refs)
    for child in node.children:
      self._collect_leaf_content(child, refs)