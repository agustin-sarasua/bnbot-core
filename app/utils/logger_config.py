import logging
import os

# Create logger instance
logger = logging.getLogger()
logging_level = os.environ.get('LOGGING_LEVEL', "DEBUG")

chain_verbose = True

logger.setLevel(logging_level)

# Define a handler and formatter
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)



# import logging
# import os
# import colorlog

# # Create logger instance
# logger = logging.getLogger()
# logging_level = os.environ.get('LOGGING_LEVEL', "DEBUG")

# chain_verbose = True

# # Create a colorlog console handler
# console_handler = colorlog.StreamHandler()
# console_handler.setLevel(logging_level)

# log_format = '%(log_color)s%(levelname)s - %(message)s'
# # Create a formatter and set it on the console handler
# formatter = colorlog.ColoredFormatter(log_format)
# console_handler.setFormatter(formatter)

# # Add the console handler to the logger
# logger.addHandler(console_handler)

