from flask_jwt_extended import get_jwt_identity
from flask_smorest import abort
from functools import wraps
from models import User
from config.extensions import db
from sqlalchemy import select

def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = db.session.scalars(select(User).where(User.id == int(get_jwt_identity()))).first()
        if current_user.role == "admin":
            return func(*args, **kwargs)
        else:
            abort(403, message="Unauthorized access.")
    return wrapper

def user_is_active(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = db.session.scalars(select(User).where(User.id == int(get_jwt_identity()))).first()
        if current_user.status == "active":
            return func(*args, **kwargs)
        elif current_user.status == "inactive":
            abort(403, message="Account deactivated.")
        elif current_user.status == "disabled":
            abort(403, message="Account suspended")
    return wrapper