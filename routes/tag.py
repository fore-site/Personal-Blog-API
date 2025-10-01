from flask.views import MethodView
from flask_smorest import Blueprint
from models.schema import TagSchema
from flask_jwt_extended import jwt_required
from middlewares.authMiddleware import user_is_active
from controllers.tag import get_tags, get_single_tag

blp = Blueprint("tags", __name__, description="Operation on Tags")

@blp.route("/tags")
class TagsRoute(MethodView):
    @blp.response(200, TagSchema(many=True))
    @blp.paginate()
    def get(self, pagination_parameters):
        return get_tags(pagination_parameters)

@blp.route("/tags/<int:tag_id>")
class TagRoute(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        return get_single_tag(tag_id)