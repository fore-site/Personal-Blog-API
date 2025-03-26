from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, select, insert, update, delete, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
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
    with Session(engine) as session:
        all_articles = session.scalars(select(Articles)).all()
    return jsonify(all_articles), 200

# GET AN ARTICLE BY ID
@app.get("/article/<article_id>")
def get_article(article_id):
    with Session(engine) as session:
        single_article = session.scalars(select(Articles).where(Articles.id == article_id)).all()
        if not single_article:
            return {"message": "resource not found"}, 400
    return jsonify(single_article), 200

# FILTER YOUR SEARCH

# CREATE AN ARTICLE
@app.post("/article")
def create_article():
    request_body = request.get_json()
    new_entry = {
        "title": request_body["title"], 
        "category": request_body["category"],
        "tags": ", ".join(request_body["tags"]), 
        "content": request_body["content"],
        "createdAt": datetime.now(), 
        "updatedAt": datetime.now()
        }
    # request.get_data()
    # request_body = request.data.decode("utf-8")
    with Session(engine) as session:
        session.execute(
            insert(Articles), [
                new_entry
            ]
        )
        session.commit()
    
    return jsonify(new_entry), 201

# UPDATE THE ENTIRE RESOURCE
@app.put("/article/<article_id>")
def update_full_article(article_id):
    request_body = request.get_json()

    # CHECK IF WHOLE RESOURCE WAS UPDATED
    try:
        updated_resource = {
            "id": article_id,
            "title": request_body["title"],
            "category": request_body["category"],
            "tags": ", ".join(request_body["tags"]),
            "content": request_body["content"],
            "updatedAt": datetime.now()
        }
    except KeyError:
        return {"message": "update entire resource in a PUT request"}, 400
    else:
        with Session(engine) as session:
        # CHECK IF ARTICLE EXISTS
            article = session.execute(select(Articles).where(Articles.id == article_id)).all()
            if not article:
                return {"message": "resource not found"}, 400
            session.execute(
                update(Articles),
                [
                    updated_resource
                ]
            )
            session.commit()
            updated_article = session.scalars(select(Articles).where(Articles.id == article_id)).all()
        return jsonify(updated_article), 201

# UPDATE PART OF THE RESOURCE
@app.patch("/article/<article_id>")
def update_part_article(article_id):
    request_body = request.get_json()
    print(type(request_body))
    return "Okay"

# DELETE ARTICLE
@app.delete("/article/<article_id>")
def delete_article(article_id):
    with Session(engine) as session:
    # CHECK IF ARTICLE EXISTS
        article = session.execute(select(Articles).where(Articles.id == article_id)).all()
        if not article:
            return {"message": "resource not found"}, 400
        session.execute(
            delete(Articles).where(Articles.id == article_id)
        )
        session.commit()
    return {"message": "Article successfully deleted"}, 200


if __name__ == "__main__":
    app.run(debug=True)