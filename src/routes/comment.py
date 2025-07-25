from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint, abort
from datetime import datetime
from sqlalchemy import select, delete, update, insert
from src.extensions import db
from models import Comment, Post
from src.schemas.schema import CommentSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

blp = Blueprint("comment", __name__, "operations on comment")

@blp.route("/comments")
class AllComments(MethodView):
    @blp.response(200, CommentSchema(many=True))
    def get(self):
        all_posts = db.session.scalars(select(Post)).all()
        return all_posts

@blp.route("/posts/<int:post_id>/comments")
class CommentRoute(MethodView):
    @blp.response(200, CommentSchema(many=True))
    def get(self, post_id):
        result = db.session.scalars(select(Comment).where(Comment.post_id == post_id)).all()
        # comment_schema = CommentSchema(many=True)
        # all_comments = comment_schema.dump(result)
        return result
    
    @jwt_required()
    @blp.arguments(CommentSchema)
    @blp.response(201, CommentSchema)
    def post(self, comment_data, post_id):
        post = db.session.scalars(select(Post).where(Post.id == post_id)).first()
        if post:
            comment_data.update({"postedAt": datetime.now(), "editedAt": datetime.now(), "post_id": post_id,
                                 "user_id": int(get_jwt_identity())})
        else:
            abort(404, message="Post not found.")
        db.session.execute(insert(Comment), [comment_data])
        db.session.commit()
        return comment_data
    
@blp.route("/posts/<int:post_id>/comments/<int:comment_id>")
class CommentIDRoute(MethodView):
    @blp.response(200, CommentSchema)
    def get(self, post_id, comment_id):
        comment = db.session.scalars(select(Comment).where(Comment.id == comment_id)).first()
        return comment

    @jwt_required()
    def delete(self, post_id, comment_id):
        comment = db.session.scalars(select(Comment).where(Comment.id == comment_id)).first()
        if comment:
            db.session.execute(delete(Comment).where(Comment.id == comment_id))
            db.commit()
            return {"message": "Comment deleted"}, 204
        abort(404, message="Comment does not exist")