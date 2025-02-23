from dotenv import dotenv_values

_env = dotenv_values(".env")

MONGO_DB_URI = _env["MONGO_DB_URI"]
FLASK_RUN_HOST = _env["FLASK_RUN_HOST"]
FLASK_RUN_PORT = _env["FLASK_RUN_PORT"]
FLASK_DEBUG = _env["FLASK_DEBUG"]
DATABASE_NAME = "aiothinkers"