from flask import Flask
from flask_smorest import Api
import os
from dotenv import load_dotenv
from src.routes.post import blp as PostBlueprint
from src.routes.user import blp as UserBlueprint
from src.routes.comment import blp as CommentBlueprint
from src.extensions import db

load_dotenv(".flaskenv")


# CREATE FLASK APP
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["API_TITLE"] = "Blog API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr/npm/swagger-ui-dist/"

    db.init_app(app)

    api = Api(app)
    with app.app_context():
        db.create_all()

    api.register_blueprint(PostBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(CommentBlueprint)

    if __name__ == "__main__":
        app.run()

create_app()