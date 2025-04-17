from src.extensions import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Posts(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    category: Mapped[str]
    tags: Mapped[str]
    content: Mapped[str]
    createdAt: Mapped[datetime]
    updatedAt: Mapped[datetime]