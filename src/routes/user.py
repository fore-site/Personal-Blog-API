from flask.views import MethodView
from flask_smorest import abort, Blueprint
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert, delete, or_, func
from src.extensions import db
from models import User
from src.schemas.schema import UserSchema

blp = Blueprint("user", __name__, description="Operation on User")

@blp.route("/user")
class UserRoute(MethodView):
    def get(self):
        result = db.session.scalars(select(User)).all()
        return result, 200
    
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user_data.update({"createdAt": datetime.now()})
        db.session.execute(insert(User), [user_data])
        db.session.commit()
        return user_data

@blp.route("/user/<int:user_id>")
class UserIDRoute(MethodView):
    def delete(self, user_id):
        user = db.session.execute(select(User).where(User.id == user_id)).all()
        if not user:
            abort(404, message="User does not exist.")
        db.session.execute(delete(User).where(User.id == user_id))
        db.session.commit()
        return "Okay", 204
