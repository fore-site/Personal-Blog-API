from db import Base
from dataclasses import dataclass

@dataclass
class Articles(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    category: Mapped[str]
    content: Mapped[str]
    createdAt: Mapped[datetime]
    updatedAt: Mapped[datetime]