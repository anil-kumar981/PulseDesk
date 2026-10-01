import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a configured logger instance with a standard formatter.
    
    Args:
        name (str): The name of the logger (usually __name__)
        
    Returns:
        logging.Logger: The configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create console handler with stdout
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        # Create standard format including the log prefix (name)
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger
