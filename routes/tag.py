from flask.views import MethodView
from flask_smorest import Blueprint
from models.schema import TagSchema
from flask_jwt_extended import jwt_required
from middlewares.authMiddleware import user_is_active, admin_only
from controllers.tag import get_tags, get_single_tag, edit_tag, delete_tag, create_tag

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
    
# ADMIN ACTIONS

@blp.route("/tags")
class AdminTagsRoute(MethodView):
    @jwt_required()
    @admin_only
    @user_is_active
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data):
        return create_tag(tag_data)

@blp.route("/tags/<int:tag_id>")
class AdminTagRoute(MethodView):
    @jwt_required()
    @admin_only
    @user_is_active
    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema)
    def put(self, tag_data, tag_id):
        return edit_tag(tag_data, tag_id)
    
    @jwt_required()
    @admin_only
    @user_is_active
    @blp.response(
        202,
        description="Deletes a tag if there are no posts linked to it",
        example={"message": "Tag deleted."}
    )
    @blp.alt_response(
        404,
        description="Tag not found."
    )
    @blp.alt_response(
        400,
        description="Returned if there are still posts linked to the tag. Tag not deleted."
    )
    def delete(self, tag_id):
        return delete_tag(tag_id)