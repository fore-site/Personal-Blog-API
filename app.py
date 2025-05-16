from flask import Flask, request
from flask_smorest import Api
import os
from dotenv import load_dotenv
from src.routes.post import blp as PostBlueprint

load_dotenv(".flaskenv")

# CREATE FLASK APP
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["API_TITLE"] = "Blog API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.0"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(PostBlueprint)

if __name__ == "__main__":
    app.run()