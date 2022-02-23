""" The idea of this script is to extract all the tickers available in the page.
To do so, all the possible combinations of three leters of the alphabet are
inputed in the search box and the results can be parsed and stored into the db."""

import itertools
import time
import pandas as pd
from db import ConnexionHandler
import selenium_funcs
from selenium_funcs import TimeoutException


def create_letter_combinations():
    """Create all the possible combinations of three letters."""
    alphabet = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
    key3 = {''.join(i) for i in itertools.product(alphabet, repeat = 3)}
    key2 = {''.join(i) for i in itertools.product(alphabet, repeat = 2)}
    key1 = alphabet
    return  set.union(key3, key2, key1)


def refresh_letter_table():
    """Input the letter combinations and set the checked flag to 0."""
    con_han = ConnexionHandler()
    letters = list(create_letter_combinations())
    df = pd.DataFrame(letters, columns =['letter_combination'])
    df["checked"] = 0

    # Truncate the table
    query = """
    TRUNCATE TABLE letter_combinations
    """
    con_han.query_database(query, 'e')

    # Insert the values
    con_han.df_to_database(df, "letter_combinations", if_exists="append")


def extract_letters():
    """Extract the not yet processed letter combinations."""
    con_han = ConnexionHandler()
    query ="""
    SELECT * FROM letter_combinations
    """
    return con_han.query_database(query, query_type='r')


def insert_or_update_ticker(ticker, ticker_desc):
    """Take a ticker and its ticker_desc and use them
    to insert or update the ticker table."""
    con_han = ConnexionHandler()
    query = f"""
    INSERT INTO tickers (ticker, ticker_desc)
    VALUES 
        ('{ticker}', '{ticker_desc}')
    ON DUPLICATE KEY UPDATE
        ticker = '{ticker}',
        ticker_desc = '{ticker_desc}'
        
    
    """
    con_han.query_database(query, query_type='e')


def update_letter_table(combination):
    """Set the combination to checked = 1."""
    con_han = ConnexionHandler()
    query=f"""
    UPDATE letter_combinations
    SET 
        checked = 1
    WHERE
        letter_combination='{combination}'
    """
    con_han.query_database(query, query_type='e')


def extract_tickers_db(only_null_desc=False):
    """Extract all the tickers already present in the DB."""
    con_han = ConnexionHandler()
    query ="""
    SELECT ticker FROM tickers
    """
    if only_null_desc:
        query += " WHERE ticker_desc IS NULL "
    return con_han.query_database(query, query_type='r')


def loop_letters(driver):
    """Loop the letter combinations using them as input to extract the
    tickers. Skip the already processed letter groups."""
    processed = set(extract_tickers_db().ticker)
    let_combs = extract_letters()
    all_combs = len(extract_letters())
    letters_to_process = list(let_combs[let_combs["checked"] == 0].letter_combination)
    already_checked = len(let_combs[let_combs["checked"] == 1].letter_combination)

    for letter_group in letters_to_process:
        selenium_funcs.input_ticker(driver, letter_group)
        time.sleep(1)
        try:
            tickers = selenium_funcs.extract_tickers(driver)
        except TimeoutException:
            tickers = {}
            pass

        for ticker in tickers:
            if ticker not in processed:
                insert_or_update_ticker(ticker, tickers[ticker])
                processed.add(ticker)

        update_letter_table(letter_group)
        already_checked += 1
        print(f"{letter_group}: --- Progress = {already_checked/all_combs * 100:.2f}%" )


def check_old_tickers(driver):
    """Check if the tickers already present in the DB are in macro_trends.
    Maybe some of them were not found by the letter combinations 
    (search engine not always work)."""
    tickers_missing_desc = set(extract_tickers_db(only_null_desc=True).ticker)
    for ticker in tickers_missing_desc:
        if selenium_funcs.ticker_url(driver, ticker):
            url = driver.current_url.split('/')
            index = url.index(ticker) + 1
            desc = url[index]
            insert_or_update_ticker(ticker, desc)


if __name__ == '__main__':
    browser = selenium_funcs.start_driver(base_page="https://www.macrotrends.net/stocks/charts/TSLA/tesla/balance-sheet?freq=Q",
                                          adblock_path="static/adblock4.43.0_0.crx")
    selenium_funcs.accept_cookies(browser)
    
    #loop_letters(browser)
    check_old_tickers(browser)
