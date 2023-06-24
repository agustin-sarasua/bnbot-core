import logging
import os

# Create logger instance
logger = logging.getLogger()
logging_level = os.environ.get('LOGGING_LEVEL', "DEBUG")

chain_verbose = True
logging_level == "DEBUG"

logger.setLevel(logging_level)

# Define a handler and formatter
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)