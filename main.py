import selenium_funcs
import table_manipulation as tm





def extract_all_tables(driver):
    """Extract and process all tables for the current page."""
    tables = {}

    for subtab in ("Income Statement", 
                   "Balance Sheet", 
                   "Cash Flow Statement",
                   "Key Financial Ratios"):

        selenium_funcs.choose_subtab(driver, subtab)
        selenium_funcs.quarterly(driver)
        g,h = selenium_funcs.parse_table_bs(driver)
        tables[subtab] = tm.reconstruct_table(g, h)

    return tables




if __name__ == '__main__':

    browser = selenium_funcs.start_driver(base_page="https://www.macrotrends.net/stocks/charts/TSLA/tesla/balance-sheet?freq=Q",
                                          adblock_path="static/adblock4.43.0_0.crx")
    selenium_funcs.accept_cookies(browser)

    #selenium_funcs.parse_table(browser)
    #t = extract_all_tables(browser, "V")
    x = extract_all_tables(browser, "V")
    selenium_funcs.find_ticker(browser, "V")
    # g,h = selenium_funcs.parse_table_bs(browser)
    # t = tm.reconstruct_table(g, h)

    
    
# from timeit import Timer
# import re
# style = "left: 790px; z-index: 738; width: 100px;"
# table = browser.find_element(By.ID, "contentjqxgrid")
# def f2(table):
#     return WebDriverWait(table, 0.2).until(
#             EC.presence_of_all_elements_located((By.XPATH, "./div[2]/div//div[@role='gridcell']"))
#             )

# def f1(table):
#     return WebDriverWait(table, 0.2).until(
#             EC.presence_of_all_elements_located((By.XPATH, ".//div[@role='gridcell']"))
#             )
# gridcell = browser.find_element_by_xpath("/html/body/div[2]/div[3]/div[4]/div/div/div[4]/div[2]/div/div[2]/div[6]")
# def f2(element):
#     return element.get_attribute('innerHTML')

# def f1(element):
#     return element.text

# t = Timer(lambda: f1(table))
# print(t.timeit(number=100))

# t = Timer(lambda: f2(table))
# print(t.timeit(number=100))