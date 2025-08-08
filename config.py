from os import path, environ
from dotenv import load_dotenv
from datetime import timedelta

basedir = path.abspath(path.dirname(__file__))

load_dotenv(path.join(basedir, ".flaskenv"))

SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"
SECRET_KEY = environ.get("SECRET_KEY")
API_TITLE = "Blog API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.1.0"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr/npm/swagger-ui-dist/"
JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)