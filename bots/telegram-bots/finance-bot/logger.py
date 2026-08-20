import logging
import socket
from logging.handlers import RotatingFileHandler

# Disable IPv6 from sockets level of Python
socket.has_ipv6 = False

def setup_logger():

    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Rotación: 5 MB por archivo, máximo 3 backups
    file_handler = RotatingFileHandler(
        "bot.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    log = logging.getLogger("PCHealthBot")
    log.setLevel(logging.INFO)

    if not log.handlers:
        log.addHandler(file_handler)
        log.addHandler(console_handler)

    # Reducir verbosidad de las librerías externas
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.WARNING)

    return log

logger = setup_logger()