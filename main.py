# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 10:39:13 2022

@author: fuertru
"""
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from utilities import chrome_appdata_folder
from exceptions import TableParsingError


def start_driver(app_name="macrotrends", download_folder=None):
    """Start the driver. Optionally a download folder can be supplied."""
    # Initialise the chrome options
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2} # Disable notifications

    # Get the appData folder to store the user
    app_data = chrome_appdata_folder()
    chromeOptions.add_argument(f"user-data-dir={app_data}/{app_name}/profile")

    #Checks for download folder
    if download_folder:
        prefs["download.default_directory"] = download_folder

    # Apply the options
    chromeOptions.add_experimental_option("prefs", prefs)

    # Initialize the driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions) 
    driver.implicitly_wait(5)

    return driver


def accept_cookies(driver):
    """Try to click on the accept all cookies."""
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Accept all')]"))
        ).click()
    except TimeoutException:
        print("No accept cookies button.")
        pass


def scroll_bar(driver, direction=None, times=1):
    """Scroll the horizontal bar."""
    # Find the scroll bar
    right_button = driver.find_element(By.ID, "jqxScrollBtnDownhorizontalScrollBarjqxgrid")
    left_button = driver.find_element(By.ID, "jqxScrollBtnUphorizontalScrollBarjqxgrid")

    if direction == "l":
        for _ in range(times):
            left_button.click()

    if direction == "r":
        for _ in range(times):
            right_button.click()



if __name__ == '__main__':
    browser = start_driver()

    browser.get("https://www.macrotrends.net/stocks/charts/GOOG/alphabet/income-statement?freq=Q")

    # Find the table
    table = browser.find_element_by_id("contentjqxgrid")

    # Find header
    header = table.find_element(By.CLASS_NAME, "jqx-grid-header")

    # Loop header



    """Each value in the table has a Z-index. This index starts at the bottom right of the table and
    increases leftwards first and upwards second. 
    Each row is identified by the role=row.
    It is possible to compute the column number by taking the max Z-index and dividing it by
    the number of rows.
    The strategy will be to extract all the z-index into a Dict and then distribute them into a matrix
    based on the number of columns and rows."""

    # Loop all the elements of the table to extract their value
    # Assign the value to a dict z-index: "value"
    # When there are no more z-index, scroll to the right
    z_index_dict = {}
    max_scroll_tries = 5
    scrolled_tries = 0
    browser.implicitly_wait(1)
    while True:
        gridcell_number = len(z_index_dict)

        for gridcell in table.find_elements(By.XPATH, ".//div[@role='gridcell']"):
            print("parsing gridcell")
            # Extract the z-index from the style of the girdcell
            z_index = [int(style.split(':')[1])
                        for style in gridcell.get_attribute("style").split(';') 
                        if style.strip().startswith("z-index")
                        ][0]

            if z_index in z_index_dict:
                continue

            # Detect the ajax-chart fields (they don't have text)
            if len(browser.find_elements(By.CLASS_NAME, "ajax-chart")):
                print("value is not None")
                # Extract the value
                value = gridcell.text

            else:
                value = None

            # Fill the dict
            z_index_dict[z_index] = value

        # Check if in the last iteration any gridcell was added
        if len(z_index_dict) == gridcell_number:
            scrolled_tries += 1
        else:
            scrolled_tries = 0

        # Check if all the z_index are in the dictionary
        if  max(z_index_dict.keys()) == len(z_index_dict):
            break

        # Check if the scroll tries expired and not all data was found
        elif scrolled_tries >= max_scroll_tries:
            raise(TableParsingError("Not all the gricells could be found."))

        scroll_bar(browser, 'r', 40)

    print(z_index_dict)

