from flask.views import MethodView
from flask_smorest import Blueprint
from models.schema import CommentSchema
from flask_jwt_extended import jwt_required
from middlewares.authMiddleware import user_is_active
from controllers.comment import get_post_comments, make_comment, get_single_comment, edit_comment, delete_comment

blp = Blueprint("comment", __name__, "operations on comment")
    
@blp.route("/posts/<int:post_id>/comments")
class CommentRoute(MethodView):
    @blp.response(200, CommentSchema(many=True))
    @blp.paginate()
    def get(self, post_id, pagination_parameters):
        return get_post_comments(post_id, pagination_parameters)
    
    @jwt_required()
    @user_is_active
    @blp.arguments(CommentSchema)
    @blp.response(201, CommentSchema)
    def post(self, comment_data, post_id):
        return make_comment(comment_data, post_id)
    
@blp.route("/posts/<int:post_id>/comments/<int:comment_id>")
class CommentIDRoute(MethodView):
    @blp.response(200, CommentSchema)
    def get(self, post_id, comment_id):
        return get_single_comment(post_id, comment_id)

    @jwt_required()
    @user_is_active
    @blp.arguments(CommentSchema)
    @blp.response(200, CommentSchema)
    def put(self, comment_data, post_id, comment_id):
        return edit_comment(comment_data, comment_id)

    @jwt_required()
    @user_is_active
    def delete(self, post_id, comment_id):
        return delete_comment(post_id, comment_id)