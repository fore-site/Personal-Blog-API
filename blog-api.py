from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, select, insert, update, delete, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import func
from dataclasses import dataclass
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv(".flaskenv")

# CREATE DATABASE
engine = create_engine("sqlite:///blog.db", echo=True)

class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True)
    }

# CREATE ARTICLES TABLE
@dataclass
class Articles(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    category: Mapped[str]
    tags: Mapped[str]
    content: Mapped[str]
    createdAt: Mapped[datetime]
    updatedAt: Mapped[datetime]

# Base.metadata.create_all(engine)

# CREATE FLASK APP
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# GET ALL ARTICLES
@app.get("/article")
def get_articles():
    if request.args:
        if len(request.args) == 1:
            key = list(request.args.keys())[0]
            value = request.args.get(key).lower()
            with Session(engine) as session:
                result = session.scalars(select(Articles).filter(func.lower(getattr(Articles, key)) == value)).all()
            return (result), 200
    with Session(engine) as session:
        all_articles = session.scalars(select(Articles)).all()
    return (all_articles), 200

# GET AN ARTICLE BY ID
@app.get("/article/<article_id>")
def get_article(article_id):
    with Session(engine) as session:
        single_article = session.scalars(select(Articles).where(Articles.id == article_id)).all()
        if not single_article:
            return {"message": "Article not found"}, 404
    return (single_article), 200

# FILTER YOUR SEARCH
@app.get("/article/filter")
def filter_result():
    print(list(request.args.keys())[0])
    return "Okay"

# CREATE AN ARTICLE
@app.post("/article")
def create_article():
    request_body = request.get_json()
    request_body["tags"] = ", ".join(request_body["tags"])
    request_body.update({"createdAt": datetime.now(), "updatedAt": datetime.now()})

    with Session(engine) as session:
        session.execute(
            insert(Articles), [
                request_body
            ]
        )
        session.commit()
    return request_body, 201

# UPDATE THE ENTIRE RESOURCE
@app.put("/article/<article_id>")
def update_full_article(article_id):
    request_body = request.get_json()

    with Session(engine) as session:
        # CHECK IF ARTICLE EXISTS
        article = session.execute(select(Articles).where(Articles.id == article_id)).all()
        if not article:
            return {"message": "Article not found"}, 404
        # CHECK IF WHOLE RESOURCE WAS UPDATED
        if len(request_body) != 4:
            return {"message": "Update all the Article values in a PUT request"}, 400
        request_body.update({"id": article_id, "updatedAt": datetime.now()})
        # CONVERT LIST DATA TYPE TO STRING
        request_body["tags"] = ", ".join(request_body["tags"])
        session.execute(update(Articles),[request_body])
        session.commit()

    return request_body, 201

# UPDATE PART OF THE RESOURCE
@app.patch("/article/<article_id>")
def update_part_article(article_id):
    request_body = request.get_json()
    with Session(engine) as session:

        # CHECK IF ARTICLE EXISTS
        article = session.execute(select(Articles).where(Articles.id == article_id)).all()
        if not article:
            return {"message": "Article not found"}, 404
        request_body.update({"id": article_id, "updatedAt": datetime.now()})
        # CONVERT LIST DATA TYPE TO STRING
        if request_body["tags"]:
            request_body["tags"] = ", ".join(request_body["tags"])
        session.execute(update(Articles), [request_body])
        session.commit()

    return request_body, 201

# DELETE ARTICLE
@app.delete("/article/<article_id>")
def delete_article(article_id):
    with Session(engine) as session:

    # CHECK IF ARTICLE EXISTS
        article = session.execute(select(Articles).where(Articles.id == article_id)).all()
        if not article:
            return {"message": "Article not found"}, 404
        session.execute(
            delete(Articles).where(Articles.id == article_id)
        )
        session.commit()
    return {"message": "Article successfully deleted"}, 200


if __name__ == "__main__":
    app.run(debug=True)