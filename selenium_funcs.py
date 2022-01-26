from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, MoveTargetOutOfBoundsException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from utilities import chrome_appdata_folder
from exceptions import TableParsingError


def start_driver(app_name="macrotrends", download_folder=None, base_page=None, adblock_path=None):
    """Start the driver. Optionally a download folder can be supplied."""
    # Initialise the chrome options
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2} # Disable notifications

    # Get the appData folder to store the user
    app_data = chrome_appdata_folder()
    chrome_options.add_argument(f"user-data-dir={app_data}/{app_name}/profile")

    # Add adblock
    if adblock_path:
        chrome_options.add_extension(adblock_path)

    #Checks for download folder
    if download_folder:
        prefs["download.default_directory"] = download_folder

    # Apply the options
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize the driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) 
    driver.implicitly_wait(5)

    # Go to the base page if provided
    if base_page:
        driver.get(base_page)

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


def find_ticker(driver, ticker):
    """Find the search box, insert the ticker name,
    parse the data elements to find the correct ticket
    and click it."""
    search_box = driver.find_element(By.ID, "jqxInput")
    search_box.send_keys(ticker)

    # Loop the child elements that appeared
    popup = driver.find_element(By.ID, "jqxInput_popup")
    for li in popup.find_elements(By.XPATH, "./li"):
        data_value = li.get_attribute("data-value")
        li_ticker = data_value.split("/")[0]

        if li_ticker.upper() == ticker.upper():
            li.click()
            return


def choose_subtab(driver, tab_name):
    """Change to the desired subtab."""
    driver.find_element(By.XPATH, f"//a[text() = '{tab_name}']").click()


def quarterly(driver):
    """Change to the Quarterly version in case the annual page was
    loaded."""
    if driver.current_url.split("/")[-1].find("?freq=Q") == -1:
        driver.get(driver.current_url + "?freq=Q")


def scroll_bar(driver, distance=150):
    """Scroll the horizontal bar."""
    # Find the scroll bar
    slider = driver.find_element_by_id('jqxScrollThumbhorizontalScrollBarjqxgrid')

    try:
        ActionChains(driver).click_and_hold(slider).move_by_offset(distance, 0).release().perform()
        return
    except MoveTargetOutOfBoundsException as e:
        print(e)
        if distance < 0:
            for _ in range(distance):
                left_button = driver.find_element(By.ID, "jqxScrollBtnUphorizontalScrollBarjqxgrid")
                left_button.click()

        if distance > 0:
            for _ in range(distance):
                right_button = driver.find_element(By.ID, "jqxScrollBtnDownhorizontalScrollBarjqxgrid")
                right_button.click()


def parse_table(driver):
    """Each value in the table has a Z-index. This index starts at the bottom right of the table and
    increases leftwards first and upwards second. 
    Each row is identified by the role=row.
    It is possible to compute the column number by taking the max Z-index and dividing it by
    the number of rows.
    The strategy will be to extract all the z-index into a Dict and then distribute them into a matrix
    based on the number of columns and rows."""

    # Find the table
    table = driver.find_element(By.ID, "contentjqxgrid")

    # Find header
    header = table.find_element(By.CLASS_NAME, "jqx-grid-header")

    # Loop all the elements of the table to extract their value
    # Assign the value to a dict z-index: "value"
    # When there are no more z-index, scroll to the right
    z_index_dict = {}
    z_index_dict_header = {}
    max_scroll_tries = 5
    scrolled_tries = 0
    driver.implicitly_wait(1)
    while True:
        gridcell_number = len(z_index_dict)

        for gridcell in table.find_elements(By.XPATH, ".//div[@role='gridcell']"):
            # Extract the z-index from the style of the girdcell
            z_index = [int(style.split(':')[1])
                        for style in gridcell.get_attribute("style").split(';') 
                        if style.strip().startswith("z-index")
                        ][0]

            if z_index in z_index_dict:
                continue

            # Detect the ajax-chart fields (they don't have text)
            if len(driver.find_elements(By.CLASS_NAME, "ajax-chart")):
                # Extract the value
                value = gridcell.text

            else:
                value = None

            # Fill the dict
            z_index_dict[z_index] = value

        # Extract info for the header
        for header in table.find_elements(By.XPATH, ".//div[@role='columnheader']"):
            z_index = [int(style.split(':')[1])
                        for style in header.get_attribute("style").split(';') 
                        if style.strip().startswith("z-index")
                        ][0]

            if z_index in z_index_dict_header:
                continue

            # Extract the value
            value = header.text

            # Fill the dict
            z_index_dict_header[z_index] = value

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

        scroll_bar(driver, 200)

    return z_index_dict, z_index_dict_header
