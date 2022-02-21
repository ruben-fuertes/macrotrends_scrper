import json
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import paramiko
import pandas as pd
from sshtunnel import SSHTunnelForwarder

JSON_FILE = "static/cred/cred.json"

class ConnexionHandler:
    """Class to handle the connexion to Mysql database."""
    def __init__(self, cred_json_path=JSON_FILE):
        self.read_cred(cred_json_path)
        self.mypkey = paramiko.RSAKey.from_private_key_file(self.ssh_cred["key_path"],
                                               self.ssh_cred["key_password"])

    def read_cred(self, cred_json_path):
        """Parse the json file with the credentials."""
        with open(cred_json_path, 'r') as f:
            cred = json.load(f)
        self.mysql_cred = cred["mysql"]
        self.ssh_cred = cred["ssh"]


    def create_engine_str(self, port):
        """Create the string necessary to create the sqlAlchemy engine."""
        string =  f'mysql://{self.mysql_cred["user"]}:{self.mysql_cred["password"]}@'
        string += f'{self.mysql_cred["host"]}:{port}/{self.mysql_cred["database"]}'
        return string


    def query_database(self, query, query_type='r'):
        """Take the credentials and run the query using a connection.
        It takes different values for the query_type:
            -"r" for reading
            -"e" for executing """
        with SSHTunnelForwarder((self.ssh_cred["host"], self.ssh_cred["port"]),
                                  ssh_username=self.ssh_cred["user"],
                                  ssh_pkey=self.mypkey,
                                  remote_bind_address=(self.mysql_cred["host"],
                                                       self.mysql_cred["port"])
                                  ) as tunnel:
            
            """cnx = pymysql.connect(user=self.mysql_cred["user"],
                                  password=self.mysql_cred["password"],
                                  host=self.mysql_cred["host"],
                                  database=self.mysql_cred["database"],
                                  port=tunnel.local_bind_port)"""
            cnx = create_engine(self.create_engine_str(port=str(tunnel.local_bind_port)))
    
            if query_type == 'r':
                return pd.read_sql_query(query, cnx)

            if query_type == 'e':
                return cnx.execute(text(query).execution_options(autocommit=True))


    def df_to_database(self, df, sql_table, if_exists="fail"):
        """Take the credentials and return a connection."""
        with SSHTunnelForwarder((self.ssh_cred["host"], self.ssh_cred["port"]),
                                  ssh_username=self.ssh_cred["user"],
                                  ssh_pkey=self.mypkey,
                                  remote_bind_address=(self.mysql_cred["host"],
                                                       self.mysql_cred["port"])
                                  ) as tunnel:
            cnx = create_engine(self.create_engine_str(port=str(tunnel.local_bind_port)))

            return df.to_sql(name=sql_table, con=cnx, if_exists=if_exists, 
                             index=False)


def get_tickers():
    """Return the tickets and their description."""
    con_han = ConnexionHandler()
    query ="""
    SELECT ticker, ticker_desc FROM tickers
    """
    return con_han.query_database(query, query_type='r')


def ticker_processed(ticker, year, quarter):
    """Check if the combination ticker/date(year, quarter) is 
    already in the database."""
    con_han = ConnexionHandler()
    query =f"""
    SELECT ticker FROM macro_trends
    WHERE
    ticker='{ticker}'
    AND year = {year}
    AND quarter_number = {quarter}
    """
    if con_han.query_database(query, query_type='r').empty:
        return False
    return True


def last_processed_date(ticker):
    """Extract the last processed date for the ticker."""
    con_han = ConnexionHandler()
    query =f"""
    SELECT ticker, year, quarter_number
    FROM macro_trends
    WHERE
    ticker='{ticker}'
    ORDER BY
    year DESC, quarter_number DESC
    LIMIT 1
    """

    df = con_han.query_database(query, query_type='r')

    if df.empty:
        return 0, 0

    return df.year[0], df.quarter_number[0]