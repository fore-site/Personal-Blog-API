from src.extensions import db
from sqlalchemy import ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import mapped_column, relationship, Mapped
from datetime import datetime

class Posts(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    tags: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    createdAt = mapped_column(TIMESTAMP)
    updatedAt = mapped_column(TIMESTAMP)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")
