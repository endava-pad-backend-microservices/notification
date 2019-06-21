import requests
import configparser
from os import environ
from Utils import Constants
import logging

class ConfigurationService:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("app.ini")
        if config.has_option("app",Constants.CONFIG_SERVER):
            self.url = config.get("app",Constants.CONFIG_SERVER)
        if(environ.get(Constants.CONFIG_SERVER)):
            self.url = environ.get(Constants.CONFIG_SERVER)

        self.req = None
        try:
            self.req = requests.get(self.url)
        except:
            logging.warning("Fail to connect to Config MS.")
            raise Exception("Fail to connect to Config MS.")

    def GetConfig(self):
        if self.req != None:
            if self.req.status_code != 200:
                raise Exception("Fail to get response from configuration MS.")
            return self.req.json()