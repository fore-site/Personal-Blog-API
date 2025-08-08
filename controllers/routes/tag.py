from flask.views import MethodView
from flask_smorest import abort, Blueprint
from datetime import datetime
from sqlalchemy import select, update, insert, delete, or_, func
from extensions import db
from models import Tag
from models.schema import TagSchema
from flask_jwt_extended import jwt_required, get_jwt_identity