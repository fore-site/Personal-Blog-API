from flask.views import MethodView
from flask_smorest import Blueprint
from models.schema import PostSchema, PostUpdateSchema, PostQuerySchema, TagSchema
from flask_jwt_extended import jwt_required
from middlewares.authMiddleware import user_is_active
from controllers.post import get_posts, make_post, get_single_post, edit_post, delete_post, link_post_tag

blp = Blueprint("posts", __name__, description="Operations on Posts")

@blp.route("/posts")
class PostRoute(MethodView):
    @blp.arguments(PostQuerySchema, location="query")
    @blp.response(200, PostSchema(many=True))
    @blp.paginate()
    def get(self, query_args, pagination_parameters):
        return get_posts(query_args, pagination_parameters)
    
    @jwt_required()
    @user_is_active
    @blp.arguments(PostSchema)
    @blp.response(201, PostSchema)
    def post(self, post_body):
        return make_post(post_body)
    
@blp.route("/posts/<int:post_id>")
class EachPost(MethodView):
    @blp.response(200, PostSchema)
    def get(self, post_id):
        return get_single_post(post_id)
    
    @jwt_required()
    @user_is_active
    @blp.arguments(PostUpdateSchema)
    @blp.response(200, PostUpdateSchema)
    def put(self, post_body, post_id):
        return edit_post(post_body, post_id)

    @jwt_required()
    @user_is_active
    def delete(self, post_id):
        return delete_post(post_id)

# LINK A POST AND A TAG
@blp.route("/posts/<int:post_id>/tags/<int:tag_id>")
class PostTagRoute(MethodView):
    @jwt_required()
    @user_is_active
    @blp.response(200, TagSchema)
    def put(self, post_id, tag_id):
        return link_post_tag(post_id, tag_id)