
"""
configures a reusable logger.

- Logs are written to both 'logs/logging.log' and the console.
- Ensures the 'logs/' directory exists.
- Provides a named logger 'datascienceLogger' for consistent logging across modules.

Usage:
    from datascience import logger
    logger.info("Message")

"""

import os 
import sys 
import logging  

# Format for all log messages
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Directory and file path for logs
log_dir = "logs"
log_filepath = os.path.join(log_dir, "logging.log")
os.makedirs(log_dir, exist_ok=True)  # Create logs/ directory if it doesn't exist

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),       # Log to file
        logging.StreamHandler(sys.stdout)        # Log to console
    ]
)

# Create a logger instance for this package
logger = logging.getLogger("datascienceLogger")
logger.info("Logger initialized for the datascience package.")
