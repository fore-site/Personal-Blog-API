from flask.views import MethodView
from flask_smorest import abort, Blueprint
from datetime import datetime
from sqlalchemy import select, update, insert, delete, or_, func
from extensions import db
from models import Tag
from models.schema import TagSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import admin_only, user_is_active

blp = Blueprint("tags", __name__, description="operation on tags")

@blp.route("/tags")
class TagsRoute(MethodView):
    @user_is_active
    @jwt_required()
    @blp.response(200, TagSchema(many=True))
    def get(self):
        all_tags = db.session.scalar(select(Tag)).all()
        return all_tags

@blp.route("/tags/<int:tag_id>")
class TagRoute(MethodView):
    @user_is_active
    @jwt_required()
    @blp.response(200, TagSchema(many=True))
    def get(self, tag_id):
        tag = db.session.scalar(select(Tag).where(Tag.id == tag_id)).first()
        return tag