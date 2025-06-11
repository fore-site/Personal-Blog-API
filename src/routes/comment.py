from flask.views import MethodView
from flask_smorest import Blueprint, abort
from datetime import datetime
from sqlalchemy import select, delete, update
from src.extensions import db
from src.schemas.schema import CommentSchema

blp = Blueprint("comment", __name__, "operations on comment")

