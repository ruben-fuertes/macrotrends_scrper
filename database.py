import json
import pymysql
import paramiko
import sshtunnel
from sshtunnel import SSHTunnelForwarder

JSON_FILE = "static/cred/cred.json"

class ConnexionHandler:
    """Class to handle the connexion to Mysql database."""
    def __init__(self, cred_json_path):
        self.read_cred(cred_json_path)
        self.create_connection()
        
        
    def read_cred(self, cred_json_path):
        """Parse the json file with the credentials."""
        with open(cred_json_path, 'r') as f:
            cred = json.load(f)
        self.mysql_cred = cred["mysql"]
        self.ssh_cred = cred["ssh"]


    def create_connection(self):
        """Take the credentials and return a connection."""
        mypkey = paramiko.RSAKey.from_private_key_file(self.ssh_cred["key_path"],
                                                       self.ssh_cred["key_password"])
        with sshtunnel.SSHTunnelForwarder((self.ssh_cred["host"], 22),
                                  ssh_username=self.ssh_cred["user"],
                                  ssh_pkey=mypkey,
                                  remote_bind_address=(self.mysql_cred["host"],
                                                       self.mysql_cred["port"])
                                  ) as tunnel:
            cnx = pymysql.connect(user=self.mysql_cred["user"],
                                  password=self.mysql_cred["password"],
                                  host=self.mysql_cred["host"],
                                  database=self.mysql_cred["database"],
                                  port=tunnel.local_bind_port)
            cursor = cnx.cursor()
        self.cnx = cnx

if __name__ == "__main__":
    x = ConnexionHandler(JSON_FILE)