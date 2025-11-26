#!/usr/bin/env python3
"""
CLI wrapper for PDFProcessor - Test PDF to image conversion

Usage examples:
  python pdf_cli.py input.pdf                          # Convert all pages, 150 DPI
  python pdf_cli.py input.pdf -d 300                   # High quality 300 DPI
  python pdf_cli.py input.pdf -d 300 -g                # 300 DPI grayscale (OCR)
  python pdf_cli.py input.pdf -p 1 5                   # Pages 1-5 only
  python pdf_cli.py input.pdf -f png                   # Output as PNG
  python pdf_cli.py input.pdf -o my_images             # Custom output directory
  python pdf_cli.py input.pdf --prefix scan -q 85      # Custom prefix, quality 85
"""

import argparse
import sys
from pathlib import Path
from pdf_processor import PDFProcessor


def parse_args():
  parser = argparse.ArgumentParser(
    description="Convert PDF to images with configurable quality settings",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  %(prog)s document.pdf                         # Basic conversion (150 DPI, JPG)
  %(prog)s document.pdf -d 300 -g               # High DPI grayscale for OCR
  %(prog)s document.pdf -p 1 10                 # First 10 pages only
  %(prog)s document.pdf -f png -d 200           # PNG format at 200 DPI
  %(prog)s document.pdf -o scans --prefix page  # Custom output location

DPI Recommendations:
  72   - Screen viewing, quick preview
  150  - Standard quality (default)
  200  - Good OCR quality
  300  - High quality, printing
  600  - Archival quality
    """
  )
  
  # Required arguments
  parser.add_argument(
    "pdf_path",
    type=str,
    help="Path to input PDF file"
  )
  
  # Output options
  parser.add_argument(
    "-o", "--output",
    type=str,
    default=None,
    help="Output directory (default: <pdf_name>_images)"
  )
  
  parser.add_argument(
    "--prefix",
    type=str,
    default="page",
    help="Filename prefix for output images (default: page)"
  )
  
  parser.add_argument(
    "--no-clean",
    action="store_true",
    help="Don't clean output directory before processing"
  )
  
  # Quality options
  parser.add_argument(
    "-d", "--dpi",
    type=int,
    default=150,
    help="Output resolution in DPI (default: 150)"
  )
  
  parser.add_argument(
    "-f", "--format",
    type=str,
    choices=["jpg", "png", "ppm"],
    default="jpg",
    help="Output image format (default: jpg)"
  )
  
  parser.add_argument(
    "-q", "--quality",
    type=int,
    default=95,
    help="JPEG quality 1-100 (default: 95, only for jpg)"
  )
  
  parser.add_argument(
    "-g", "--grayscale",
    action="store_true",
    help="Convert to grayscale (smaller files, good for OCR)"
  )
  
  # Page selection
  parser.add_argument(
    "-p", "--pages",
    type=int,
    nargs=2,
    metavar=("START", "END"),
    help="Page range to process (1-indexed, inclusive). Example: -p 1 5"
  )
  
  # Verbosity
  parser.add_argument(
    "-v", "--verbose",
    action="store_true",
    help="Show detailed processing information"
  )
  
  return parser.parse_args()


def main():
  args = parse_args()
  
  # Validate input PDF
  pdf_path = Path(args.pdf_path)
  if not pdf_path.exists():
    print(f"Error: PDF file not found: {pdf_path}", file=sys.stderr)
    sys.exit(1)
  
  if not pdf_path.suffix.lower() == ".pdf":
    print(f"Warning: File doesn't have .pdf extension: {pdf_path}")
  
  # Determine output directory
  if args.output:
    output_dir = Path(args.output)
  else:
    output_dir = Path(f"{pdf_path.stem}_images")
  
  # Show configuration if verbose
  if args.verbose:
    print("\n" + "="*60)
    print("PDF Processor Configuration")
    print("="*60)
    print(f"Input PDF:      {pdf_path}")
    print(f"Output dir:     {output_dir}")
    print(f"DPI:            {args.dpi}")
    print(f"Format:         {args.format.upper()}")
    print(f"Quality:        {args.quality}" + (" (ignored for non-JPG)" if args.format != "jpg" else ""))
    print(f"Grayscale:      {args.grayscale}")
    print(f"Page range:     {f'{args.pages[0]}-{args.pages[1]}' if args.pages else 'All pages'}")
    print(f"Prefix:         {args.prefix}")
    print(f"Clean output:   {not args.no_clean}")
    print("="*60 + "\n")
  
  try:
    # Create processor
    processor = PDFProcessor(
      dpi=args.dpi,
      image_format=args.format,
      quality=args.quality,
      grayscale=args.grayscale
    )
    
    # Convert PDF
    page_range = tuple(args.pages) if args.pages else None
    
    images = processor.convert_to_images(
      pdf_path=pdf_path,
      output_dir=output_dir,
      page_range=page_range,
      clean_output=not args.no_clean,
      prefix=args.prefix
    )
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✓ SUCCESS: Converted {len(images)} pages")
    print(f"{'='*60}")
    print(f"Output location: {output_dir.absolute()}")
    
    if images:
      total_size = sum(img.stat().st_size for img in images) / (1024 * 1024)  # MB
      avg_size = total_size / len(images)
      print(f"Total size:      {total_size:.2f} MB")
      print(f"Avg per image:   {avg_size:.2f} MB")
      
      if args.verbose:
        print(f"\nFirst image:     {images[0].name}")
        print(f"Last image:      {images[-1].name}")
    
    print(f"{'='*60}\n")
    
  except ValueError as e:
    print(f"Error: Invalid configuration - {e}", file=sys.stderr)
    sys.exit(1)
  except RuntimeError as e:
    print(f"Error: Processing failed - {e}", file=sys.stderr)
    sys.exit(1)
  except KeyboardInterrupt:
    print("\n\nInterrupted by user", file=sys.stderr)
    sys.exit(130)
  except Exception as e:
    print(f"Error: Unexpected error - {e}", file=sys.stderr)
    if args.verbose:
      import traceback
      traceback.print_exc()
    sys.exit(1)


if __name__ == "__main__":
  main()