import logging
from logging.handlers import TimedRotatingFileHandler
import pathlib
import os
import sys
from dotenv import load_dotenv
load_dotenv()

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent

# logging config
FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —"
    "%(funcName)s:%(lineno)d — %(message)s")
LOG_DIR = PACKAGE_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "tox_block_api.log"

def get_console_handler() -> logging.StreamHandler:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler

def get_file_handler() -> TimedRotatingFileHandler:
    file_handler = TimedRotatingFileHandler(
        LOG_FILE, when="midnight")
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.WARNING)
    return file_handler

def get_logger(logger_name: str) -> logging.Logger:
    """Get logger with prepared handlers."""

    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.INFO)

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False

    return logger

# config for Flask environment
class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("FLASK_CONFIG_SECRET_KEY")
    SERVER_PORT = 5000
    CORS_HEADERS = "Content-Type"


class ProductionConfig(Config):
    DEBUG = False
    SERVER_ADDRESS: os.environ.get("SERVER_ADDRESS", "0.0.0.0")
    SERVER_PORT: os.environ.get("PORT", "5000")


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
