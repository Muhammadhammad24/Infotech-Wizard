import logging
import sys
from typing import Optional
from app.core.config import get_settings

settings = get_settings()


def setup_logging(
    name: Optional[str] = None,
    level: Optional[str] = None
) -> logging.Logger:
    """Configure and return a logger instance."""
    logger = logging.getLogger(name or __name__)
    
    # Use provided level or default from settings
    log_level = level or settings.log_level
    logger.setLevel(getattr(logging, log_level))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger


# Create default logger
logger = setup_logging("chatbot")