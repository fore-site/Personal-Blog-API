from flask_smorest import abort
from datetime import datetime
from sqlalchemy import select, delete, insert, update, func
from config.extensions import db
from models import Comment, Post, User
from flask_jwt_extended import get_jwt_identity

def get_post_comments(post_id, pagination_parameters):
    pagination_parameters.item_count = db.session.scalar(select(func.count()).select_from(Comment))
    limit = pagination_parameters.page_size
    offset = pagination_parameters.first_item
    all_comments = db.session.scalars(select(Comment)
                                      .where(Comment.post_id == post_id)
                                      .limit(limit)
                                      .offset(offset)).all()
    return all_comments

def make_comment(comment_data, post_id):
    post = db.session.scalars(select(Post).where(Post.id == post_id)).first()
    if post:
        comment_data.update({"postedAt": datetime.now(), "editedAt": datetime.now(), "post_id": post_id,
             "user_id": int(get_jwt_identity())})
    else:
        abort(404, message="Post not found.")
    db.session.execute(insert(Comment), [comment_data])
    db.session.commit()
    return comment_data

def get_single_comment(post_id, comment_id):
    comment = db.session.scalars(select(Comment).where(Comment.id == comment_id, Comment.post_id == post_id)).first()
    return comment

def edit_comment(comment_body, comment_id):
    comment = db.session.scalars(select(Comment).where(Comment.id == comment_id)).first()
    if comment:
        if comment.user_id == int(get_jwt_identity()):
            comment_body.update({"id": comment_id, "editedAt": datetime.now()})
            db.session.execute(update(Comment),[comment_body])
            db.session.commit()
            return comment_body
        else:
            abort(403, message="Cannot edit another user's comment")
    else:
        abort(404, message="Comment not found.")

def delete_comment(post_id, comment_id):
    comment = db.session.scalars(select(Comment).where(Comment.id == comment_id, Comment.post_id == post_id)).first()
    user = db.session.scalars(select(User).where(User.id == int(get_jwt_identity()))).first()
    if comment:
        if comment.user_id == int(get_jwt_identity()) or user.role == "admin":
            db.session.execute(delete(Comment).where(Comment.id == comment_id))
            db.commit()
            return {"message": "Comment deleted"}, 204
        else:
            abort(403, message="Cannot delete another user's comment.")
    abort(404, message="Comment does not exist")