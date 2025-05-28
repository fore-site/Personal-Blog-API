from src.extensions import db
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import Integer, String, TIMESTAMP
from typing import List
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    createdAt = mapped_column(TIMESTAMP)
    posts = relationship("Posts", back_populates="user", lazy="dynamic")
