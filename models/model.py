from src.extensions import db
from sqlalchemy import ForeignKey, func, select
from sqlalchemy.orm import mapped_column, relationship, Mapped, column_property
from datetime import datetime
from typing import List

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    createdAt: Mapped[datetime] = mapped_column()
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")

class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    postedAt: Mapped[datetime] = mapped_column()
    editedAt: Mapped[datetime] = mapped_column()
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="comments")

class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    category: Mapped[str]
    tags: Mapped[str]
    content: Mapped[str]
    createdAt: Mapped[datetime] = mapped_column()
    updatedAt: Mapped[datetime] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")
    comment_count: Mapped[int] = column_property(
        select(func.count(Comment.id))
        .where(Comment.post_id == id)
        .correlate_except(Comment)
        .scalar_subquery()
    )