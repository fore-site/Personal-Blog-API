from flask_jwt_extended import get_jwt_identity
from flask_smorest import abort
from functools import wraps
from models import User
from extensions import db
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
        if current_user.is_active:
            return func(*args, **kwargs)
        else:
            abort(403, message="Account deactivated.")
    return wrapper