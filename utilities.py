import sys
import os
import logging
from datetime import datetime

def working_directory():
    """Return the working directory."""
    try:
        work_dir = sys._MEIPASS
    except AttributeError:
        work_dir = os.getcwd()
    return work_dir


def chrome_appdata_folder():
    """Return the appdata folder for chrome."""
    return os.getenv('LOCALAPPDATA') + r'\Google\Chrome'


def appdata_folder():
    """Create if it does not exist and return the appdata folder for the app."""
    app_data_folder= os.getenv('LOCALAPPDATA') + r'\Salesforce_extraction_tool'
    if not os.path.isdir(app_data_folder):
        os.mkdir(app_data_folder)
    return app_data_folder


def create_logs_dir():
    """Create logs dir if it does not exist."""
    if not os.path.isdir("logs"):
        os.mkdir("logs")


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


def setup_loggers():
    """Set up two loggers, one for the normal operation and the other for the
    errored tickers."""
    create_logs_dir()
    now = datetime.now().strftime("%Y%m%d_%H_%M_%S")
    basic_logger = setup_logger('basic_logger', f'logs/{now}__info.log')
    error_logger = setup_logger('error_logger', f'logs/{now}__errored_tickers.log',
                                level=logging.WARNING)

    return basic_logger, error_logger
