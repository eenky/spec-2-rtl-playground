import typer
from pathlib import Path
from typing import Optional
import sys
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from pdf_processor import PDFProcessor, PDFExportConfig

app = typer.Typer(add_completion=False)

@app.command()
def main(
  input: Path = typer.Option(..., "--input", "-i", exists=True, dir_okay=False),
  output: Optional[Path] = typer.Option(None, "--output", "-o"),
  dpi: int = typer.Option(150, "--dpi")
):
  """Convert PDF to Images (Standard)."""
  print(f"--- Starting Processing: {input.name} ---")
  config = PDFExportConfig(dpi=dpi, image_format="png")
  try:
    with PDFProcessor(input) as processor:
      images = processor.convert_to_images(config, output_dir=output)
      print(f"Success! Generated {len(images)} images.")
  except Exception as e:
    print(f"Fatal Error: {e}")
    raise typer.Exit(code=1)

@app.command()
def ocr(
  input_dir: Path = typer.Option(..., "--input", "-i", exists=True, file_okay=False),
  output_dir: Path = typer.Option(..., "--output-dir", "-o"),
  extract_timing: bool = typer.Option(False, "--extract-timing", help="Enable Cloud Logic Extraction.")
):
  """
  Run OlmOCR on images. Smartly detects and extracts timing logic.
  """
  try:
    from ocr_engine import OlmOCRProcessor, GeminiTimingExtractor
    ocr_engine = OlmOCRProcessor()
  except ImportError as e:
    print(f"Error: Missing ML dependencies. {e}")
    raise typer.Exit(1)
    
  gemini_extractor = None
  if extract_timing:
    try:
      gemini_extractor = GeminiTimingExtractor()
      print("[INFO] Cloud Vision initialized.")
    except Exception as e:
      print(f"[WARN] Cloud Vision unavailable: {e}")
      extract_timing = False

  if not output_dir.exists():
    output_dir.mkdir(parents=True)

  images = sorted(list(input_dir.glob("*.png")))
  print(f"--- Processing {len(images)} pages ---")

  full_text_buffer = []

  for i, img in enumerate(images):
    print(f"[{i+1}/{len(images)}] Reading {img.name}...", end=" ", flush=True)
    
    try:
      # A. Local Text OCR
      page_text = ocr_engine.process_image(img)
      
      md_path = output_dir / f"{img.stem}.md"
      with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"\n\n{page_text}")
      
      full_text_buffer.append(f"\n\n\n{page_text}")
      print("Done.")

      # B. Diagram Detection Logic
      if extract_timing:
        keywords = ["timing", "switching", "waveform", "figure"]
        has_keyword = any(k in page_text.lower() for k in keywords)
        
        if has_keyword:
          print(f"      [?] Hints found. Verifying visual presence...", end=" ")
          if ocr_engine.has_visual_diagram(img):
            print("YES.")
            print(f"      [⚡] Sending to Gemini for Context Extraction...")
            try:
              logic_data = gemini_extractor.analyze_diagram(img)
              
              json_path = output_dir / f"{img.stem}_timing.json"
              with open(json_path, "w", encoding="utf-8") as f:
                json.dump(logic_data, f, indent=2)
                
              print(f"      [✓] Logic extracted: Mode='{logic_data.get('operating_mode', 'Unknown')}'")
            except Exception as e:
              print(f"      [X] Extraction failed: {e}")
          else:
            print("NO.")

    except Exception as e:
      print(f"\nError processing {img.name}: {e}")

  full_path = output_dir / "_full_datasheet.md"
  with open(full_path, "w", encoding="utf-8") as f:
    f.write("\n".join(full_text_buffer))
  print(f"\n--- Complete! Output in {output_dir} ---")

@app.command()
def build_context(
  input_dir: Path = typer.Option(..., "--input-dir", "-i", exists=True),
  output_dir: Path = typer.Option(..., "--output-dir", "-o", help="Folder to save contexts."),
  force: bool = typer.Option(False, "--force", "-f", help="Force re-classification even if cached.")
):
  """
  Analyze pages using both Markdown text AND Gemini Timing Logic (if available).
  """
  try:
    from rtl_context import PageClassifier, KnowledgeTreeBuilder
    import json
  except ImportError as e:
    print(f"Error: {e}")
    raise typer.Exit(1)
  
  if not output_dir.exists():
    output_dir.mkdir(parents=True)

  # --- Phase 1: Classification (Local Qwen) ---
  flat_path = output_dir / "rtl_context_flat.json"
  flat_manifest = []

  if flat_path.exists() and not force:
    print(f"--- Phase 1: Page Classification (Skipped) ---")
    print(f"[Cache] Found existing context at {flat_path.name}. Loading...")
    with open(flat_path, "r", encoding="utf-8") as f:
      flat_manifest = json.load(f)
    print(f"Loaded {len(flat_manifest)} pages from cache.")
  else:
    print("--- Phase 1: Page Classification (Ollama) ---")
    classifier = PageClassifier(model_name="qwen3:14b")
    
    files = sorted(list(input_dir.glob("*.md")))
    files = [f for f in files if not f.name.startswith("_")]
    
    print(f"Analyzing {len(files)} pages...")
    
    for f in files:
      print(f"Classifying {f.name}...", end=" ", flush=True)
      
      with open(f, "r", encoding="utf-8") as file_handle:
        content = file_handle.read()
        
      # Context Injection
      timing_json_path = input_dir / f"{f.stem}_timing.json"
      
      context_injection = ""
      if timing_json_path.exists():
        try:
          with open(timing_json_path, "r") as jf:
            data = json.load(jf)
          mode = data.get("operating_mode", "Unknown Mode")
          clock = data.get("clock_domain", {}).get("signal", "Unknown Clock")
          
          context_injection = (
            f"\n[METADATA FROM GEMINI VISION]\n"
            f"Verified Operating Mode: {mode}\n"
            f"Clock Signal: {clock}\n"
            f"Contains Timing Diagram: YES\n"
            f"----------------------------------------\n"
          )
          print(f"[+JSON Mode: {mode}]", end=" ")
        except Exception as e:
          print(f"[JSON Error: {e}]", end=" ")

      full_analysis_content = context_injection + content
      
      analysis = classifier.analyze_page(f.stem, full_analysis_content)
      print(f"[{analysis.page_type.value.upper()}] Score: {analysis.relevance_score}")
      
      if analysis.relevance_score >= 4:
        flat_manifest.append(analysis.model_dump())

    with open(flat_path, "w", encoding="utf-8") as f:
      json.dump(flat_manifest, f, indent=2)
    print(f"-> Flat context saved to {flat_path.name}")

  # --- Phase 2: Tree Construction (Cloud Gemini) ---
  if flat_manifest:
    print("\n--- Phase 2: Knowledge Tree Construction (GROVE) ---")
    builder = KnowledgeTreeBuilder(model_name="gemini-2.5-flash")
    tree = builder.build_tree(flat_manifest)
    
    if tree:
      tree_path = output_dir / "rtl_knowledge_tree.json"
      with open(tree_path, "w", encoding="utf-8") as f:
        f.write(tree.model_dump_json(indent=2))
      print(f"-> 🌳 Hierarchy built and saved to {tree_path.name}")
    else:
      print("-> Failed to build tree structure (Check API Key).")
  else:
    print("-> No relevant pages found.")

  print("\n--- Context Build Complete ---")

@app.command()
def list_options(
  context_dir: Path = typer.Option(..., "--context-dir", "-c", exists=True, help="Path to context folder.")
):
  """Read the Knowledge Tree and display available RTL configurations."""
  try:
    from rtl_context import TreeNavigator
  except ImportError as e:
    print(f"Error: {e}")
    raise typer.Exit(1)

  tree_path = context_dir / "rtl_knowledge_tree.json"
  if not tree_path.exists():
    print(f"Error: No tree found at {tree_path}. Run 'build-context' first.")
    raise typer.Exit(1)

  navigator = TreeNavigator(tree_path)
  options = navigator.list_configurations()

  print(f"\n--- Available Configurations for {navigator.root.title} ---")
  print(f"Device Description: {navigator.root.description}\n")

  if not options:
    print("[!] No selectable sub-modes found. The tree might be flat or malformed.")
    return

  for idx, opt in enumerate(options):
    print(f"{idx + 1}. {opt['name']}")
    print(f"   ID:        {opt['id']}")
    print(f"   Logic:     {opt['description']}")
    print(f"   Condition: {opt['condition']}")
    print("")

  print(f"To generate RTL, you will select an ID (e.g. '{options[0]['id']}')")

@app.command()
def generate_spec(
  config_name: str = typer.Option(..., "--config", "-c", help="The configuration to spec (e.g. '3-wire busy')."),
  context_dir: Path = typer.Option(..., "--context-dir", "-d", exists=True),
  md_dir: Path = typer.Option(..., "--md-dir", "-m", exists=True),
  output: Path = typer.Option("requirements.md", "--output", "-o")
):
  """Generate a Formal Requirements Specification (Markdown)."""
  try:
    from rtl_generator import SpecGenAgent
  except ImportError as e:
    print(f"Error: {e}")
    raise typer.Exit(1)

  agent = SpecGenAgent(context_dir=context_dir, md_dir=md_dir)
  
  print(f"--- Drafting Requirements for: {config_name} ---")
  try:
    prompt = f"Generate a full Requirements Specification for the '{config_name}' mode of the AD7980."
    spec_text = agent.run(prompt)
    
    with open(output, "w", encoding="utf-8") as f:
      f.write(spec_text)
      
    print(f"\n--- Spec Generation Complete ---")
    print(f"Saved to: {output.absolute()}")
    
  except Exception as e:
    print(f"Agent Failure: {e}")
    import traceback
    traceback.print_exc()
    raise typer.Exit(1)

@app.command()
def generate(
  prompt: str = typer.Option(..., "--prompt", "-p", help="What RTL to generate."),
  context_dir: Path = typer.Option(..., "--context-dir", "-c", exists=True),
  md_dir: Path = typer.Option(..., "--md-dir", "-m", exists=True, help="Folder with markdown/json pages.")
):
  """Generate SystemVerilog using the Knowledge Tree Agent (LangGraph)."""
  try:
    from rtl_generator import RTLAgent
  except ImportError as e:
    print(f"Error: {e}")
    raise typer.Exit(1)

  agent = RTLAgent(context_dir=context_dir, md_dir=md_dir)
  
  try:
    code = agent.run(prompt)
    
    output_file = Path("generated_rtl.sv")
    with open(output_file, "w", encoding="utf-8") as f:
      f.write(code)
      
    print(f"\n--- Generation Complete ---")
    print(f"Code saved to: {output_file.absolute()}")
    
  except Exception as e:
    print(f"Agent Failure: {e}")
    import traceback
    traceback.print_exc()
    raise typer.Exit(1)

if __name__ == "__main__":
  app()