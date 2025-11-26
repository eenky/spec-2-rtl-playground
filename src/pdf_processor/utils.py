import logging
import sys

def setup_logger(name: str = "PDFProcessor", level: int = logging.INFO) -> logging.Logger:
  """
  Configures a simple logger that outputs to console.
  
  Format: [LEVEL] Message
  """
  logger = logging.getLogger(name)
  
  # Avoid adding handlers multiple times if this is called repeatedly
  if not logger.handlers:
    logger.setLevel(level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
      fmt="[%(levelname)s] %(message)s",
      datefmt="%H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
  return logger