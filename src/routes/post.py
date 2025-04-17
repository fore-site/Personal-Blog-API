from flask import request
from flask.views import MethodView
from flask_smorest import abort, Api, Blueprint
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert, delete, or_, func
from extensions import engine

blp = Blueprint("posts", __name__, description="Operations on posts")

@blp.route("/post")
class posts(MethodView):
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
                            return {"message": "post not found"}, 404
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
            all_posts = session.scalars(select(Posts)).all()
            return all_posts, 200
    
    def post(self):
        request_body = request.get_json()
        request_body["tags"] = ", ".join(request_body["tags"])
        request_body.update({"createdAt": datetime.now(), "updatedAt": datetime.now()})
            
        with Session(engine) as session:
            session.execute(
                insert(posts), [
                    request_body
                ]
            )
            session.commit()
        return request_body, 201