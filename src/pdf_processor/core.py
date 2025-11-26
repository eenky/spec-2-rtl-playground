from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
import fitz  # PyMuPDF
from .utils import setup_logger

# --- Configuration Object ---

@dataclass
class PDFExportConfig:
  """
  Configuration for the PDF to Image conversion process.
  Default: 150 DPI, PNG format.
  """
  dpi: int = 150
  image_format: str = "png"

# --- Main Processor Facade ---

class PDFProcessor:
  def __init__(self, file_path: Path):
    # 1. Setup Logger
    self.logger = setup_logger()
    
    self.file_path = Path(file_path)
    self.document: Optional[fitz.Document] = None
    
    # Define default output directory: ./filename_images/
    self.default_output_dir = self.file_path.parent / f"{self.file_path.stem}_images"
    
    self.logger.debug(f"Initialized processor for: {self.file_path}")

  def __enter__(self):
    """Context Manager entry: Opens the file resource."""
    self.open()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    """Context Manager exit: Guarantees cleanup."""
    if exc_type:
      self.logger.error(f"Error occurred during processing: {exc_val}")
    self.close()

  def open(self) -> None:
    """Opens the PDF file safely."""
    if not self.file_path.exists():
      self.logger.error(f"File not found: {self.file_path}")
      raise FileNotFoundError(f"Could not find {self.file_path}")
      
    try:
      self.document = fitz.open(self.file_path)
      self.logger.info(f"Opened {self.file_path.name} ({self.document.page_count} pages)")
    except Exception as e:
      self.logger.critical(f"Failed to open PDF: {e}")
      raise

  def close(self) -> None:
    """Closes the PDF file handle."""
    if self.document:
      self.document.close()
      self.document = None
      self.logger.debug("Document closed.")

  def convert_to_images(self, config: PDFExportConfig) -> List[Path]:
    """
    Converts all pages in the PDF to images based on the config.
    Returns a list of paths to the created images.
    """
    if not self.document:
      raise RuntimeError("Document is not open. Use 'with PDFProcessor(...)'.")

    # 1. Ensure output directory exists
    if not self.default_output_dir.exists():
      self.default_output_dir.mkdir(parents=True)
      self.logger.info(f"Created output directory: {self.default_output_dir}")

    generated_files = []

    # 2. Iterate through pages
    for page_num, page in enumerate(self.document):
      try:
        # Calculate Matrix for DPI (72 is base PDF DPI)
        # zoom = 300 / 72 = 4.16x
        zoom = config.dpi / 72
        matrix = fitz.Matrix(zoom, zoom)
        
        # Render page to pixel map
        pix = page.get_pixmap(matrix=matrix)
        
        # Construct filename: page_001.png
        filename = f"page_{page_num + 1:03d}.{config.image_format}"
        output_path = self.default_output_dir / filename
        
        # Save to disk
        pix.save(output_path)
        generated_files.append(output_path)
        
        self.logger.debug(f"Saved {filename}")
        
      except Exception as e:
        self.logger.error(f"Failed to convert page {page_num + 1}: {e}")

    self.logger.info(f"Conversion complete. {len(generated_files)} images saved.")
    return generated_files