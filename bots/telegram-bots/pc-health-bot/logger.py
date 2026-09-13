# Add principal libraries
import logging
import socket
from logging.handlers import RotatingFileHandler

# Disable IPv6 from sockets level of Python
socket.has_ipv6 = False

# Create the logger function
def setup_logger():

    # Format the log message
    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Configure the side of file, 5 MB for file, max 3 backups
    file_handler = RotatingFileHandler(
        "bot.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )

    # Set the file handler    
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    # Set the console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    # Set log levels
    log = logging.getLogger("PCHealthBot")
    log.setLevel(logging.INFO)

    # Check and set handlers when it doesn't exits
    if not log.handlers:
        log.addHandler(file_handler)
        log.addHandler(console_handler)

    # Reduce extern libraries verbosity
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.WARNING)

    return log

# Start the function
logger = setup_logger()