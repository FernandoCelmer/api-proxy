import logging

from json import loads
from os import environ, path
from proxy.core.file import File


class Settings:

    def __init__(self) -> None:
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except Exception as error:
            logging.error(error)

    @staticmethod
    def load_data():
        """Sets up configuration for the app
        """
        return {
            "proxy": loads(File.read(path_file=environ.get("PROXY", "./proxy/data/proxy.json"))),
            "users": loads(File.read(path_file=environ.get("USERS", "./proxy/data/users.json"))),
        }

    @staticmethod
    def load_variables():
        """Sets up configuration for the app
        """
        variables = {
            "debug": bool(environ.get("DEBUG", 1)),
            "environment": environ.get("ENVIRONMENT", 'development'),
            "base_dir": path.abspath(path.dirname(__file__)),
            "url_proxy": environ.get("URL_PROXY", 'http://172.16.238.10:8000'),
            "url_prometheus": environ.get("URL_PROMETHEUS", 'http://172.16.238.11:9090'),
            "nosql_database_url": environ.get("NOSQL_DATABASE_URL", 'mongodb://172.16.238.12:27017')
        }

        for config in variables:
            globals()[config] = variables[config]

        return variables
