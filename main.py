from sqlalchemy.exc import IntegrityError
import selenium_funcs as sf
import db
import table_manipulation as tm
from utilities import setup_loggers
from exceptions import EmptyPageError


def extract_all_tables(driver):
    """Extract and process all tables for the current page."""
    tables = {}

    for subtab in ("Income Statement",
                   "Balance Sheet",
                   "Cash Flow Statement",
                   "Key Financial Ratios"):

        sf.quarterly(driver)
        sf.choose_subtab(driver, subtab)
        if sf.check_for_empty_table(driver):
            raise EmptyPageError
        g,h = sf.parse_table_bs(driver)
        tables[subtab] = tm.reconstruct_table(g, h)

    return tables


def main(driver, days_from_last_update=0):
    """Main func."""
    log1,log2 = setup_loggers()

    cnx = db.ConnexionHandler()
    sf.accept_cookies(driver)
    tickers = set(db.get_tickers().ticker)
    processed = db.tickers_data_last_n_days(days_from_last_update)

    # Remove the tickers already in the database
    tickers = tickers.difference(processed)

    for ticker in tickers:
        # Update the last processed date
        db.update_last_processed_date(ticker)
        log1.info(f"Processing ticker: {ticker}")
        if not sf.ticker_url(driver, ticker):
            log1.info("Skpipping: ticker not in macrotrends.")
            continue
        if sf.check_for_empty_table(driver):
            log1.info("Skpipping: ticker has an empty table in macrotrends.")
            continue

        last_date = tm.extract_yq(sf.exctract_last_date(driver))
        last_processed = db.last_processed_date(ticker)

        if not last_date == last_processed:
            try:
                t = tm.postprocess_tables(extract_all_tables(driver), ticker)
            except EmptyPageError:
                log2.exception(f"Processing ticker: {ticker} rised an error.")
                log1.error(f"Processing ticker: {ticker} rised an EmptyPageError error.")
                continue
            if last_processed != (0, 0):
                # Filter the df to keep only the additions
                date_filter = last_processed[0] * 100 + last_processed[1]
                t = t[t.year.dt.year * 100 + t.quarter_number > date_filter]

            try:
                cnx.df_to_database(t, 'macro_trends', if_exists='append')
                log1.info("Data inserted into the DB.")
            except IntegrityError:
                log2.exception(f"Processing ticker: {ticker} rised an error.")
                log1.error(f"Processing ticker: {ticker} rised an error.")
        else:
            log1.info("Skipping: it's already in the DB.")




if __name__ == '__main__':
    browser = sf.start_driver(base_page="https://www.macrotrends.net/stocks/charts/TSLA/tesla/balance-sheet?freq=Q",
                                          adblock_path="static/adblock4.43.0_0.crx")
    main(browser, days_from_last_update=20)

    #sf.accept_cookies(browser)

    #sf.parse_table(browser)
    #t = extract_all_tables(browser, "V")
    #x = extract_all_tables(browser)
    #sf.find_ticker(browser, "V")
    # g,h = sf.parse_table_bs(browser)
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
