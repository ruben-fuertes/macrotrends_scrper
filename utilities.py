import sys
import os

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
