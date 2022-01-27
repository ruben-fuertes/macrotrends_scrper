import selenium_funcs
import table_manipulation as tm

def extract_all_tables(driver, ticker):
    """Extract and process all tables for a ticker."""
    selenium_funcs.find_ticker(driver, ticker)

    tables  = {}

    for subtab in ("Income Statement", 
                   "Balance Sheet", 
                   "Cash Flow Statement",
                   "Key Financial Ratios"):

        selenium_funcs.choose_subtab(driver, subtab)
        selenium_funcs.quarterly(driver)
        g,h = selenium_funcs.parse_table(driver)
        tables[subtab] = tm.reconstruct_table(g, h)

    return tables



if __name__ == '__main__':

    browser = selenium_funcs.start_driver(base_page="https://www.macrotrends.net/stocks/charts/TSLA/tesla/balance-sheet?freq=Q",
                                          adblock_path="static/adblock4.43.0_0.crx")
    selenium_funcs.accept_cookies(browser)

    #selenium_funcs.parse_table(browser)
    t = extract_all_tables(browser, "V")
