from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase, MappedAsDataclass):
    pass

db = SQLAlchemy(model_class=Base)

