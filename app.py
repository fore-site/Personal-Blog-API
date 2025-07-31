from blocklist import jwt_redis_blocklist
from controllers.routes.post import blp as PostBlueprint
from controllers.routes.user import blp as UserBlueprint
from controllers.routes.comment import blp as CommentBlueprint
from extensions import db
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask import Flask

# CREATE FLASK APP
def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_token_revoked(jwt_header, jwt_payload):
        return jwt_payload["jti"] in jwt_redis_blocklist
    
    api = Api(app)
    with app.app_context():
        db.create_all()

    import warnings
    warnings.filterwarnings("ignore", message="Multiple schemas resolved to the name ")
    
    api.register_blueprint(PostBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(CommentBlueprint)

    if __name__ == "__main__":
        app.run()

create_app()