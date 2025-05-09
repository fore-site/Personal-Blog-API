from sqlalchemy import create_engine, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from datetime import datetime

class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True)
    }

engine = create_engine("sqlite:///blog.db", echo=True)

# Base.metadata.create_all(engine)
