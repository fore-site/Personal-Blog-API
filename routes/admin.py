from middlewares.authMiddleware import admin_only, user_is_active
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from models.schema import UserSchema
from models.schema import TagSchema
from controllers.admin import get_all_users, suspend_user, restore_user, create_tag, edit_tag, delete_tag, unlink_post_tags

blp = Blueprint("admin", __name__, "Operations on admin")

@blp.route("/admin/users")
class AllUsersRoute(MethodView):
    @jwt_required()
    @admin_only
    @user_is_active
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return get_all_users()

@blp.route("/admin/users/<int:user_id>/suspend")
class AdminUserRoute(MethodView):
    @jwt_required(verify_type=False)
    @admin_only
    @user_is_active
    def patch(self, user_id):
        return suspend_user(user_id)
        
@blp.route("/admin/users/<int:user_id>/restore")
class AdminRestoreUser(MethodView):
    @jwt_required()
    @admin_only
    @user_is_active
    def patch(self, user_id):
        return restore_user(user_id)

@blp.route("/admin/tags")
class AdminTagsRoute(MethodView):
    @jwt_required()
    @admin_only
    @user_is_active
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data):
        return create_tag(tag_data)

@blp.route("/admin/tags/<int:tag_id>")
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
    
# LINK AND UNLINK POST AND TAG
@blp.route("/admin/posts/<int:post_id>/tags/<int:tag_id>")
class PostTagRoute(MethodView):
    @jwt_required()
    @admin_only
    @user_is_active
    @blp.response(200, TagSchema)
    def patch(self, post_id, tag_id):
        return unlink_post_tags(post_id, tag_id)