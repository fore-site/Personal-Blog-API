from blocklist import jwt_redis_blocklist, ACCESS_EXPIRES
from controllers.permissions import admin_only, user_is_active
from flask import jsonify
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from models.schema import UserSchema
from extensions import db
from sqlalchemy import select, delete, update
from models import User, Post, Comment

blp = Blueprint("admin", __name__, "Operations on admin")

@blp.route("/admin/users")
class AllUsersRoute(MethodView):
    @user_is_active
    @jwt_required()
    @admin_only
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = db.session.scalars(select(User)).all()
        return users

@blp.route("/admin/users/<int:user_id>")
class AdminUserRoute(MethodView):
    @user_is_active
    @jwt_required(verify_type=False)
    @admin_only
    def patch(self, user_id):
        user = db.session.scalars(select(User).where(User.id == user_id)).first()
        if not user:
            abort(404, message="User not found.")
        elif not user.is_active:
            abort(409, message="User already deactivated.")
        else:
            db.session.execute(update(User), [{"id": user_id, "is_active": False}])
            db.session.commit()
            return jsonify({"message": "User successfully deactivated."}), 202
    
@blp.route("/admin/posts/<int:post_id>")
class AdminPostRoute(MethodView):
    @user_is_active
    @jwt_required()
    @admin_only
    def delete(self, post_id):
        post = select(Post).where(Post.id == post_id)
        if not post:
            abort(404, message="Post not found.")
        else:
            db.session.execute(delete(Post).where(Post.id == post_id))
            db.session.commit()
            return({"message": "Post deleted"}), 204

@blp.route("/admin/posts/<int:post_id>/comments/<int:comment_id>")
class AdminCommentRoute(MethodView):
    @user_is_active
    @jwt_required()
    @admin_only
    def delete(self, post_id, comment_id):
        comment = select(Comment).where(Comment.id == comment_id, Comment.post_id == post_id)
        if comment:
            db.session.execute(delete(Comment).where(Comment.id == comment_id, Comment.post_id == post_id))
            db.session.commit()
            return jsonify({"message": "Comment deleted."}), 204
        abort(404, message="Comment not found.")