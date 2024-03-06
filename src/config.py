from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET_AUTH = os.environ.get("SECRET_AUTH")

SECRET_KEY: str = os.environ.get("SECRET_KEY", default="secret_key")
ALGORITHM: str = os.environ.get("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)