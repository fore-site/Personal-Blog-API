from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint, abort
from datetime import datetime
from sqlalchemy import select, delete, update, insert
from src.extensions import db
from models import Comment
from src.schemas.schema import CommentSchema
from flask_jwt_extended import jwt_required

blp = Blueprint("comment", __name__, "operations on comment")

@blp.route("/comment")
class CommentRoute(MethodView):
    # @blp.response(200, CommentSchema(many=True))
    def get(self):
        result = db.session.scalars(select(Comment)).all()
        comment_schema = CommentSchema(many=True)
        all_comments = comment_schema.dump(result)
        return all_comments, 200
    
    @blp.arguments(CommentSchema)
    def post(self, comment_data):
        comment_data.update({"postedAt": datetime.now(), "editedAt": datetime.now()})
        db.session.execute(insert(Comment), [comment_data])
        db.session.commit()
        return comment_data, 201
    
@blp.route("/comment/<int:comment_id>")
class CommentIDRoute(MethodView):
    @jwt_required
    def delete(self, comment_id):
        comment = db.session.scalars(select(Comment).where(Comment.id == comment_id)).first()
        if comment:
            db.session.execute(delete(Comment).where(Comment.id == comment_id))
            db.commit()
            return {"message": "Comment deleted"}, 204
        abort(404, message="Comment does not exist")