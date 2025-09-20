from utils.blocklist import jwt_redis_blocklist, ACCESS_EXPIRES
from middlewares.authMiddleware import admin_only, user_is_active
from flask import jsonify
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from models.schema import UserSchema
from config.extensions import db
from sqlalchemy import select, delete, update, insert
from models import User, Post, Comment, Tag
from models.schema import TagSchema

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

@blp.route("/admin/users/<int:user_id>/suspend")
class AdminUserRoute(MethodView):
    @user_is_active
    @jwt_required(verify_type=False)
    @admin_only
    def patch(self, user_id):
        user = db.session.scalars(select(User).where(User.id == user_id)).first()
        if not user:
            abort(404, message="User not found.")
        elif user.status == "inactive" or user.status == "disabled":
            abort(409, message="User already deactivated.")
        else:
            db.session.execute(update(User), [{"id": user_id, "status": "disabled"}])
            db.session.commit()
            return jsonify({"message": "User successfully deactivated."}), 202
        
@blp.route("/admin/users/<int:user_id>/restore")
class AdminRestoreUser(MethodView):
    @jwt_required()
    @user_is_active
    @admin_only
    def patch(self, user_id):
        user = select(User).where(User.id == user_id)
        if not user:
            abort(404, message="User not found")
        elif user.status == "active":
            abort(409, message="Account already restored")
        else:
            db.session.execute(User, [{"id": user_id, "status": "active"}])
            db.session.commit()
            return jsonify({"message": "User successfully restored"}), 200
    
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

@blp.route("/admin/tags")
class AdminTagsRoute(MethodView):
    @user_is_active
    @jwt_required()
    @admin_only
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema(many=True))
    def post(self, tag_data):
        db.session.execute(insert(Tag), [tag_data])
        db.session.commit()
        return tag_data

@blp.route("/admin/tags/<int:tag_id>")
class AdminTagRoute(MethodView):
    @user_is_active
    @jwt_required()
    @admin_only
    @blp.arguments(TagSchema)
    def patch(self, tag_data, tag_id):
        tag = select(Tag).where(Tag.id == tag_id)
        if tag:
            db.session.execute(update(Tag), [{"id": tag_id, "name": tag_data["name"]}])
            db.session.commit()
            return jsonify({"message": "Tag updated"}), 200
        else:
            abort(404, message="Tag not found.")
    
    @user_is_active
    @jwt_required()
    @admin_only
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
        tag = db.get_or_404(Tag, tag_id)
        if not tag.posts:
            db.session.execute(delete(Tag).where(Tag.id == tag_id))
            db.session.commit()
            return {"message": "Tag deleted."}
        else:
            abort(400, message="There are posts associated with this tag. Tag cannot be deleted.")

# LINK POST AND TAG
@blp.route("/admin/posts/<int:post_id>/tags/<int:tag_id>")
class PostTagRoute(MethodView):
    @user_is_active
    @jwt_required()
    @admin_only
    @blp.response(200, TagSchema)
    def post(self, post_id, tag_id):
        post = db.get_or_404(Post, post_id)
        tag = db.get_or_404(Tag, tag_id)
        post.tags.append(tag)
        db.session.commit()
        return tag

    @user_is_active
    @jwt_required()
    @admin_only
    @blp.response(200, TagSchema)
    def delete(self, post_id, tag_id):
        post = db.get_or_404(Post, post_id)
        tag = db.get_or_404(Tag, tag_id)
        post.tags.remove(tag)
        db.session.commit
        return jsonify({"message": "Post removed from tag.", "tag": tag})
    