from flask_smorest import abort
from datetime import datetime
from sqlalchemy import desc, select, update, insert, delete, or_, func
from config.extensions import db
from models import Post, Tag, User, PostTags
from flask_jwt_extended import get_jwt_identity

def get_posts(query_args, pagination_parameters):
    pagination_parameters.item_count = db.session.scalar(select(func.count()).select_from(Post))
    limit = pagination_parameters.page_size
    offset = pagination_parameters.first_item
    if query_args:
        # MAKE A LIST OF THE KEYS IN THE KEY-VALUE PAIRS OF THE QUERY ARGUMENT
        keys = list(query_args.keys())
        # IF MULTIPLE URL ARGUMENTS
        result = select(Post)
        for each_key in keys:
        # GET EACH VALUE OF THE QUERY ARGUMENT
            if each_key == "tags":
                value = query_args.get(each_key)
                result = result.join(Post.tags).where(Tag.name == value)
            elif each_key == "q":
                value = query_args.get(each_key).lower()
                result = result.filter(or_(
                Post.title.icontains(value), Post.content.icontains(value)))
        result = db.session.scalars(result
                                    .limit(limit)
                                    .offset(offset)).all()
        if result:
            return result
        else:
            abort(404, message="Post not found.")
    all_posts = db.session.scalars(select(Post)
                                   .limit(pagination_parameters.page_size)
                                   .offset(pagination_parameters.first_item)
                                   .order_by(desc(Post.createdAt))).all()
    return all_posts

def make_post(post_body):
    post_body.update({"createdAt": datetime.now(), "updatedAt": datetime.now(), "user_id": int(get_jwt_identity())})
    db.session.execute(insert(Post), [post_body])
    db.session.commit()
    return post_body, 201

def get_single_post(post_id):
    single_post = db.session.scalars(select(Post).where(Post.id == post_id)).first()
    if not single_post:
        abort(404, message="Post not found.")
    else:
        return single_post
    
def edit_post(post_body, post_id):
    # CHECK IF post EXISTS
    post = db.session.scalars(select(Post).where(Post.id == post_id)).first()
    if not post:
        abort(404, message="Post not found.")
    else:
        if post.user_id == int(get_jwt_identity()):
            post_body.update({"id": post_id, "updatedAt": datetime.now()})
            db.session.execute(update(Post), [post_body])
            db.session.commit()
            return post_body
        else:
            abort(403, message="Cannot edit another user's post.")

def delete_post(post_id):
    # CHECK IF POST EXISTS
    post = db.session.scalars(select(Post).where(Post.id == post_id)).first()
    user = db.session.scalars(select(User).where(User.id == int(get_jwt_identity()))).first()
    if not post:
        abort(404, message="Post not found.")
    if post.user_id == int(get_jwt_identity()) or user.role == "admin":
        db.session.execute(delete(Post).where(Post.id == post_id))
        db.session.commit()
        return {"message": "Post deleted."}, 204
    else:
        abort(403, message="Cannot delete another user's post")

def link_post_tag(post_id, tag_id):
    user = db.get_or_404(User, int(get_jwt_identity()))
    post = db.get_or_404(Post, post_id)
    if post.user_id == user.id or user.role == "admin":
        tag = db.get_or_404(Tag, tag_id)
        post.tags.append(tag)
        db.session.commit()
        return tag
    else:
        abort(403, message="Cannot link tag to another user's post.")
