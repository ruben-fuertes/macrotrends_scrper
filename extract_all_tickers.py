""" The idea of this script is to extract all the tickers available in the page.
To do so, all the possible combinations of three leters of the alphabet are
inputed in the search box and the results can be parsed and stored into the db."""

import itertools
import pandas as pd
from db import ConnexionHandler
#import selenium_funcs


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


def extract_tickers():
    """Extract all the tickers already present in the DB."""
    con_han = ConnexionHandler()
    query ="""
    SELECT ticker FROM tickers
    WHERE ticker_desc IS NOT NULL
    """
    return con_han.query_database(query, query_type='r')


def extract_processed_letters():
    """Extract the already processed letter combinations."""
    con_han = ConnexionHandler()
    query ="""
    SELECT letter_combination FROM letter_combinations
    WHERE checked = 1
    """
    return con_han.query_database(query, query_type='r')


