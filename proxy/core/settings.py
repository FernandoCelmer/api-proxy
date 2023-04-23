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
            "DEBUG": bool(environ.get("DEBUG", 1)),
            "ENVIRONMENT": environ.get("ENVIRONMENT", 'development'),
            "BASE_DIR": path.abspath(path.dirname(__file__)),
            "URL_PROYX": environ.get("URL_PROMETHEUS", 'http://172.16.238.10:8000'),
            "URL_PROMETHEUS": environ.get("URL_PROMETHEUS", 'http://172.16.238.11:9090'),
        }

        for config in variables:
            globals()[config] = variables[config]

        return variables
