from src.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from datetime import datetime
from typing import List

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    createdAt: Mapped[datetime] = mapped_column()
    posts: Mapped[List["Posts"]] = relationship(back_populates="user")

class Posts(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column()
    tags: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    createdAt: Mapped[datetime] = mapped_column()
    updatedAt: Mapped[datetime] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
