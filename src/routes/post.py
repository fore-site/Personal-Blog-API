from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert, delete, or_, func
from src.extensions import engine
from models import Posts
from src.schemas.post import PostSchema, PostPutSchema, PostUpdateSchema


blp = Blueprint("posts", __name__, description="Operations on Posts")

def key_is_tags(key):
    value = request.args.get(key).lower()
    if "-" in value:
        values = value.split("-")
        result = select(Posts)
        for each_tag in values:
            result = result.filter(func.lower
            (getattr(Posts, key)).icontains(each_tag))
        return result
    result = select(Posts).filter(func.lower
    (getattr(Posts, key)).icontains(value))
    return result

@blp.route("/post")
class Post(MethodView):
    def get(self):
        if request.args:
            keys = list(request.args.keys())

        # IF ONLY ONE ARGUMENT
            if len(request.args) == 1:
                key = keys[0]
                if key == "tags":
                    with Session(engine) as session:
                        result = session.scalars(key_is_tags(key)).all()
                        if result:
                            return result, 200
                        else:
                            abort(404, message="Post not found.")
                elif key == "term":
                    value = request.args.get(key).lower()
                    with Session(engine) as session:
                        result = select(Posts).filter(or_(
                        Posts.tags.icontains(value), Posts.content.icontains(value), Posts.category.contains(value)))
                        result = session.scalars(result).all()
                        if result:
                            return result, 200
                        else:
                            return {"message": "post not found"}, 404
                value = request.args.get(key).lower()
                with Session(engine) as session:
                    result = session.scalars(select(Posts).filter(func.lower(getattr(Posts, key)) == value)).all()
                if result:
                    return result, 200
                else:
                    return {"message": "post not found"}, 404
        
        # IF MULTIPLE URL ARGUMENTS
            with Session(engine) as session:
                result = select(Posts)
            for each_key in keys:
                if each_key == "tags":
                    result = key_is_tags(each_key)
                elif each_key == "term":
                    value = request.args.get(each_key).lower()
                    result = select(Posts).filter(or_(
                    Posts.tags.icontains(value), Posts.content.icontains(value), Posts.category.contains(value)))
                else:
                    result = result.filter(func.lower(getattr(Posts, each_key))
                    == request.args.get(each_key).lower())
            result = session.scalars(result).all()
            if result:
                return result, 200
            else:
                return {"message": "post not found"}, 404
        with Session(engine) as session:
            all_Posts = session.scalars(select(Posts)).all()
            return all_Posts, 200
    
    @blp.arguments(PostSchema)
    @blp.response(201, PostSchema)
    def post(self, post_body):
        post_body["tags"] = ", ".join(post_body["tags"])
        post_body.update({"createdAt": datetime.now(), "updatedAt": datetime.now()})
            
        with Session(engine) as session:
            session.execute(
                insert(Posts), [
                    post_body
                ]
            )
            session.commit()
        post_body["tags"] = post_body["tags"].split(",")
        return post_body

@blp.route("/post/<int:post_id>")
class EachPost(MethodView):
    def get(self, post_id):
        with Session(engine) as session:
            single_post = session.scalars(select(Posts).where(Posts.id == post_id)).all()
        if not single_post:
            return {"message": "post not found"}, 404
        return single_post, 200
    
    @blp.arguments(PostPutSchema)
    @blp.response(200, PostPutSchema)
    def put(self, post_body, post_id):
        with Session(engine) as session:
            # CHECK IF post EXISTS
            post = session.execute(select(Posts).where(Posts.id == post_id)).all()
            if not post:
                return {"message": "post not found"}, 404
            post_body.update({"id": post_id, "updatedAt": datetime.now()})
            # CONVERT LIST DATA TYPE TO STRING
            post_body["tags"] = ", ".join(post_body["tags"])
            session.execute(update(Posts),[post_body])
            session.commit()
        # DO THIS SO IT DOES NOT BREAK INTO INDIVIDUAL LETTERS WHEN RETURNED
        post_body["tags"] = post_body["tags"].split(",")

        return post_body

    @blp.arguments(PostUpdateSchema)
    @blp.response(200, PostUpdateSchema)
    def patch(self, post_body, post_id):
        with Session(engine) as session:
            # CHECK IF post EXISTS
            post = session.execute(select(Posts).where(Posts.id == post_id)).all()
            if not post:
                return {"message": "post not found"}, 404
            post_body.update({"id": post_id, "updatedAt": datetime.now()})
            # CONVERT LIST DATA TYPE TO STRING
            if post_body.get("tags"):
                post_body["tags"] = ", ".join(post_body["tags"])
            session.execute(update(Posts), [post_body])
            session.commit()

        return post_body, 200

    def delete(self, post_id):
        with Session(engine) as session:

        # CHECK IF POST EXISTS
            post = session.execute(select(Posts).where(Posts.id == post_id)).all()
            if not post:
                abort(404, message="Post not found.")
            session.execute(
                delete(Posts).where(Posts.id == post_id)
            )
            session.commit()
        return "Ok", 204
