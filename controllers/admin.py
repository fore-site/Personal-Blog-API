from flask import jsonify
from flask_smorest import abort
from config.extensions import db
from sqlalchemy import select, delete, update, insert, func
from models import User, Post, Tag
from flask_jwt_extended import get_jwt_identity

def get_all_users(pagination_parameters):
    pagination_parameters.item_count = select(func.count()).select_from(User)
    users = db.session.scalars(select(User)).all()
    print(pagination_parameters.first_item, pagination_parameters.last_item)
    return users

def suspend_user(user_id):
    user = db.session.scalars(select(User).where(User.id == user_id)).first()
    if not user:
        abort(404, message="User not found.")
    elif user.status == "inactive" or user.status == "disabled":
        abort(409, message="User already deactivated.")
    elif int(get_jwt_identity()) == user_id:
        abort(403, message="Cannot suspend one's self.")
    else:
        db.session.execute(update(User), [{"id": user_id, "status": "disabled"}])
        db.session.commit()
        return jsonify({"message": f"User {user.username} successfully deactivated."}), 202
    
def restore_user(user_id):
    user = db.session.scalars(select(User).where(User.id == user_id)).first()
    if not user:
        abort(404, message="User not found")
    elif user.status == "active":
        abort(409, message="Account already restored")
    else:
        db.session.execute(update(User), [{"id": user_id, "status": "active"}])
        db.session.commit()
        return jsonify({"message": f"User {user.username} successfully restored"}), 200

def create_tag(tag_data):
    db.session.execute(insert(Tag), [tag_data])
    db.session.commit()
    return tag_data

def edit_tag(tag_data, tag_id):
    tag = select(Tag).where(Tag.id == tag_id)
    if tag:
        db.session.execute(update(Tag), [{"id": tag_id, "name": tag_data["name"]}])
        db.session.commit()
        return jsonify({"message": "Tag updated"}), 200
    else:
        abort(404, message="Tag not found.")

def delete_tag(tag_id):
    tag = db.get_or_404(Tag, tag_id)
    if not tag.posts:
        db.session.execute(delete(Tag).where(Tag.id == tag_id))
        db.session.commit()
        return {"message": "Tag deleted."}
    else:
        abort(400, message="There are posts associated with this tag. Tag cannot be deleted.")

def unlink_post_tags(post_id, tag_id):
    post = db.get_or_404(Post, post_id)
    tag = db.get_or_404(Tag, tag_id)
    post.tags.remove(tag)
    db.session.commit
    return jsonify({"message": "Post removed from tag.", "tag": tag})
    