import os
import shutil
from pathlib import Path
from typing import List, Optional
import fitz  # PyMuPDF


class PDFProcessor:
  """Converts PDF documents to images with configurable quality settings."""
  
  def __init__(
    self, 
    dpi: int = 150,
    image_format: str = "jpg",
    quality: int = 95,
    grayscale: bool = False
  ):
    """
    Args:
      dpi: Output resolution (72=screen, 150=standard, 300=high quality)
      image_format: Output format ('jpg', 'png', 'ppm')
      quality: JPEG quality (1-100, only applies to jpg)
      grayscale: Convert to grayscale (useful for OCR, smaller files)
    """
    if dpi <= 0:
      raise ValueError("DPI must be positive")
    if quality < 1 or quality > 100:
      raise ValueError("quality must be between 1 and 100")
      
    # Convert DPI to zoom factor (72 DPI is base)
    self.zoom_factor = dpi / 72.0
    self.zoom_matrix = fitz.Matrix(self.zoom_factor, self.zoom_factor)
    self.image_format = image_format.lower()
    self.quality = quality
    self.grayscale = grayscale
    self.dpi = dpi

  def convert_to_images(
    self, 
    pdf_path: Path, 
    output_dir: Path,
    page_range: Optional[tuple[int, int]] = None,
    clean_output: bool = True,
    prefix: str = "page"
  ) -> List[Path]:
    """
    Converts PDF pages to images.
    
    Args:
      pdf_path: Path to input PDF file
      output_dir: Directory for output images
      page_range: Optional (start, end) tuple for page selection (1-indexed, inclusive)
      clean_output: Whether to clean output_dir before processing
      prefix: Filename prefix for output images (default: "page")
      
    Returns:
      List of paths to generated images, sorted by page number
      
    Raises:
      FileNotFoundError: If PDF doesn't exist
      RuntimeError: If PDF processing fails
    """
    if not pdf_path.exists():
      raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    # Prepare output directory
    if clean_output and output_dir.exists():
      shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    image_paths = []
    
    # Use context manager for automatic cleanup
    with fitz.open(pdf_path) as doc:
      total_pages = len(doc)
      
      # Determine page range
      start_page, end_page = self._validate_page_range(
        page_range, total_pages
      )
      
      print(f"[PDF] Processing pages {start_page}-{end_page} "
            f"of {total_pages} from {pdf_path.name}...")
      print(f"[PDF] Settings: {self.dpi} DPI, {self.image_format.upper()}, "
            f"{'grayscale' if self.grayscale else 'color'}")
      
      for page_num in range(start_page - 1, end_page):
        try:
          image_path = self._process_page(
            doc[page_num], 
            page_num + 1,
            output_dir,
            prefix
          )
          image_paths.append(image_path)
          
          # Progress indicator
          if (page_num - start_page + 2) % 10 == 0:
            print(f"[PDF] Processed {page_num - start_page + 2}/"
                  f"{end_page - start_page + 1} pages...")
            
        except Exception as e:
          print(f"[PDF] Error processing page {page_num + 1}: {e}")
          raise RuntimeError(
            f"Failed to process page {page_num + 1}"
          ) from e
    
    print(f"[PDF] Successfully saved {len(image_paths)} images to {output_dir}")
    return sorted(image_paths)
  
  def _process_page(
    self, 
    page: fitz.Page, 
    page_number: int,
    output_dir: Path,
    prefix: str
  ) -> Path:
    """Process a single page and save as image."""
    # Get pixmap with zoom
    pix = page.get_pixmap(
      matrix=self.zoom_matrix,
      alpha=False  # No transparency for smaller file sizes
    )
    
    # Convert to grayscale if requested
    if self.grayscale and pix.n > 2:  # n=1 is already grayscale
      pix = fitz.Pixmap(fitz.csGRAY, pix)
    
    # Zero-padded filename for proper sorting
    image_filename = f"{prefix}_{page_number:03d}.{self.image_format}"
    image_path = output_dir / image_filename
    
    # Save with quality settings for JPEG
    if self.image_format == "jpg":
      pix.save(str(image_path), jpg_quality=self.quality)
    else:
      pix.save(str(image_path))
    
    return image_path
  
  @staticmethod
  def _validate_page_range(
    page_range: Optional[tuple[int, int]], 
    total_pages: int
  ) -> tuple[int, int]:
    """Validate and normalize page range."""
    if page_range is None:
      return 1, total_pages
    
    start, end = page_range
    
    if start < 1 or end > total_pages or start > end:
      raise ValueError(
        f"Invalid page range ({start}, {end}) for "
        f"{total_pages}-page document"
      )
    
    return start, end


# Simple CLI when run directly
if __name__ == "__main__":
  import argparse
  
  parser = argparse.ArgumentParser(description="Convert PDF to images")
  parser.add_argument("-i", "--input", required=True, help="Input PDF file")
  parser.add_argument("-o", "--output", help="Output directory (default: <pdf_name>_images)")
  parser.add_argument("-d", "--dpi", type=int, default=150, help="DPI (default: 150)")
  parser.add_argument("-f", "--format", choices=["jpg", "png", "ppm"], default="jpg", help="Image format")
  parser.add_argument("-q", "--quality", type=int, default=95, help="JPEG quality 1-100")
  parser.add_argument("-g", "--grayscale", action="store_true", help="Convert to grayscale")
  parser.add_argument("-p", "--pages", nargs=2, type=int, metavar=("START", "END"), help="Page range")
  parser.add_argument("--prefix", default="page", help="Filename prefix")
  
  args = parser.parse_args()
  
  # Setup paths
  pdf_path = Path(args.input)
  if not pdf_path.exists():
    print(f"Error: PDF not found: {pdf_path}")
    exit(1)
  
  # Auto-generate output directory name from PDF name
  if args.output:
    output_dir = Path(args.output)
  else:
    output_dir = Path(f"{pdf_path.stem}_images")
  
  # Create processor and convert
  processor = PDFProcessor(
    dpi=args.dpi,
    image_format=args.format,
    quality=args.quality,
    grayscale=args.grayscale
  )
  
  page_range = tuple(args.pages) if args.pages else None
  
  images = processor.convert_to_images(
    pdf_path=pdf_path,
    output_dir=output_dir,
    page_range=page_range,
    prefix=args.prefix
  )
  
  print(f"\n✓ Converted {len(images)} pages to {output_dir.absolute()}")