from json import loads
from logging import info
from os import environ, path

from proxy.core.file import File


class Settings:

    def __init__(self) -> None:
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except Exception as error:
            info(str(error))

    @staticmethod
    def load():
        """Sets up configuration for the app
        """

        variables = {
            "DEBUG": bool(environ.get("DEBUG", 1)),
            "ENVIRONMENT": environ.get("ENVIRONMENT", 'development'),
            "DATABASE_URL": environ.get("DATABASE_URL", "sqlite:///./sql_app.db"),
            "BASE_DIR": path.abspath(path.dirname(__file__)),
            "PROXY": loads(File.read(path_file="./proxy/data/proxy.json")),
            "USERS": loads(File.read(path_file="./proxy/data/users.json"))
        }

        for config in variables:
            globals()[config] = variables[config]

        return variables
