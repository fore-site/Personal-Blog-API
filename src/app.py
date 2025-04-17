from flask import Flask, request
from sqlalchemy import select, insert, update, delete, or_, func
from datetime import datetime
import os
from dotenv import load_dotenv
from models.post import posts
from src.extensions import engine

load_dotenv(".flaskenv")

def key_is_tags(key):
    value = request.args.get(key).lower()
    if "-" in value:
        values = value.split("-")
        result = select(posts)
        for each_tag in values:
            result = result.filter(func.lower
            (getattr(posts, key)).icontains(each_tag))
        return result
    result = select(posts).filter(func.lower
    (getattr(posts, key)).icontains(value))
    return result


# CREATE FLASK APP
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# GET A POST BY ID
@app.get("/post/<int:post_id>")
def get_post(post_id):
    with Session(engine) as session:
        single_post = session.scalars(select(posts).where(posts.id == post_id)).all()
        if not single_post:
            return {"message": "post not found"}, 404
    return single_post, 200

# UPDATE THE ENTIRE RESOURCE
@app.put("/post/<post_id>")
def update_full_post(post_id):
    request_body = request.get_json()

    with Session(engine) as session:
        # CHECK IF post EXISTS
        post = session.execute(select(posts).where(posts.id == post_id)).all()
        if not post:
            return {"message": "post not found"}, 404
        # CHECK IF WHOLE RESOURCE WAS UPDATED
        if len(request_body) != 4:
            return {"message": "Update all the post values in a PUT request"}, 400
        request_body.update({"id": post_id, "updatedAt": datetime.now()})
        # CONVERT LIST DATA TYPE TO STRING
        request_body["tags"] = ", ".join(request_body["tags"])
        session.execute(update(posts),[request_body])
        session.commit()

    return request_body, 200

# UPDATE PART OF THE RESOURCE
@app.patch("/post/<post_id>")
def update_part_post(post_id):
    request_body = request.get_json()
    with Session(engine) as session:

        # CHECK IF post EXISTS
        post = session.execute(select(posts).where(posts.id == post_id)).all()
        if not post:
            return {"message": "post not found"}, 404
        request_body.update({"id": post_id, "updatedAt": datetime.now()})
        # CONVERT LIST DATA TYPE TO STRING
        if request_body["tags"]:
            request_body["tags"] = ", ".join(request_body["tags"])
        session.execute(update(posts), [request_body])
        session.commit()

    return request_body, 200

# DELETE POST
@app.delete("/post/<post_id>")
def delete_post(post_id):
    with Session(engine) as session:

    # CHECK IF POST EXISTS
        post = session.execute(select(posts).where(posts.id == post_id)).all()
        if not post:
            return {"message": "post not found"}, 404
        session.execute(
            delete(posts).where(posts.id == post_id)
        )
        session.commit()
    return 204


if __name__ == "__main__":
    app.run()