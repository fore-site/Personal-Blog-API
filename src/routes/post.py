from flask.views import MethodView
from flask import jsonify
from flask_smorest import abort, Blueprint
from datetime import datetime
from sqlalchemy import select, update, insert, delete, or_, func
from src.extensions import db
from models import Post
from src.schemas.schema import PostSchema, PostUpdateSchema, PostQuerySchema
from flask_jwt_extended import jwt_required

blp = Blueprint("posts", __name__, description="Operations on Posts")

@blp.route("/post")
class PostRoute(MethodView):
    @blp.arguments(PostQuerySchema, location="query")
    def get(self, query_args):
        if query_args:
            # MAKE A LIST OF THE KEYS IN THE KEY-VALUE PAIRS OF THE QUERY ARGUMENT
            keys = list(query_args.keys())
        # IF MULTIPLE URL ARGUMENTS
            result = select(Post)
            for each_key in keys:
                # GET EACH VALUE OF THE QUERY ARGUMENT
                value = query_args.get(each_key)
                if each_key == "tags":
                    result = result.filter(func.lower(getattr(Post, each_key)).icontains(value))
                elif each_key == "term":
                    value = query_args.get(each_key).lower()
                    result = select(Post).filter(or_(
                    Post.tags.icontains(value), Post.content.icontains(value)))
                else:
                    result = result.filter(func.lower(getattr(Post, each_key))
                    == query_args.get(each_key).lower())
            result = db.session.scalars(result).all()
            if result:
                return result, 200
            else:
                abort(404, message="Post not found.")
        all_posts = db.session.scalars(select(Post)).all()
        schema = PostSchema(many=True)
        result = schema.dump(all_posts)
        return (result), 200
    
    @jwt_required
    @blp.arguments(PostSchema)
    @blp.response(201, PostSchema)
    def post(self, post_body):
        post_body.update({"createdAt": datetime.now(), "updatedAt": datetime.now()})
        db.session.execute(insert(Post), [post_body])
        db.session.commit()
        return post_body, 201

@blp.route("/post/<int:post_id>")
class EachPost(MethodView):
    def get(self, post_id):
        single_post = db.session.scalars(select(Post).where(Post.id == post_id)).all()
        if not single_post:
            abort(404, message="Post not found.")
        post_schema = PostSchema(many=True)
        result = post_schema.dump(single_post)
        return result, 200
    
    @jwt_required
    @blp.arguments(PostUpdateSchema)
    @blp.response(200, PostUpdateSchema)
    def patch(self, post_body, post_id):
            # CHECK IF post EXISTS
        post = db.session.scalars(select(Post).where(Post.id == post_id)).first()
        if not post:
            abort(404, message="Post not found.")
        post_body.update({"id": post_id, "updatedAt": datetime.now()})
        db.session.execute(update(Post), [post_body])
        db.session.commit()
        return post_body, 200

    @jwt_required
    def delete(self, post_id):
        # CHECK IF POST EXISTS
        post = db.session.scalars(select(Post).where(Post.id == post_id)).all()
        if not post:
            abort(404, message="Post not found.")
        db.session.execute(delete(Post).where(Post.id == post_id))
        db.session.commit()
        return "Ok", 204
