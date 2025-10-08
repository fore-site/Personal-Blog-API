from utils.blocklist import jwt_redis_blocklist
from routes.post import blp as PostBlueprint
from routes.user import blp as UserBlueprint
from routes.comment import blp as CommentBlueprint
from routes.tag import blp as TagBlueprint
from config.extensions import db
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask import Flask
from middlewares.limiter import limiter

# CREATE FLASK APP
def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config/config.py")

    limiter.init_app(app)
    db.init_app(app)
    jwt = JWTManager(app)

    limiter.limit("10/second")(UserBlueprint)
    limiter.limit("10/second")(PostBlueprint)
    limiter.limit("10/second")(CommentBlueprint)
    limiter.exempt(TagBlueprint)


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
    api.register_blueprint(TagBlueprint)

    return app