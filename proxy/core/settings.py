from logging import info
from os import environ, path


def set_up():
    """Sets up configuration for the app
    """
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception as error:
        info(str(error))

    config = {
        "DEBUG": bool(environ.get("DEBUG", 1)),
        "ENVIRONMENT": environ.get("ENVIRONMENT", 'development'),
        "BASE_DIR": path.abspath(path.dirname(__file__))
    }
    return config
