from flask.views import MethodView
from flask_smorest import abort, Blueprint
from datetime import datetime
from sqlalchemy import select, update, insert, delete
from src.extensions import db
from models import User
from src.schemas.schema import UserSchema, UserLoginSchema
from werkzeug import security

blp = Blueprint("user", __name__, description="Operation on User")

@blp.route("/register")
class UserRoute(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user_data.update({"createdAt": datetime.now(), "password": security.generate_password_hash(user_data["password"], "scrypt", 8)})
        db.session.execute(insert(User), [user_data])
        db.session.commit()
        return user_data

@blp.route("/user/<int:user_id>")
class UserIDRoute(MethodView):
    def get(self, user_id):
        single_user = db.session.execute(select(User).where(User.id == user_id)).all()
        user_schema = UserSchema(many=True)
        result = user_schema.dump(single_user)
        return result, 200

    def delete(self, user_id):
        user = db.session.execute(select(User).where(User.id == user_id)).all()
        if not user:
            abort(404, message="User does not exist.")
        db.session.execute(delete(User).where(User.id == user_id))
        db.session.commit()
        return "Okay", 204
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = db.session.scalars(select(User).where(User.username == user_data["username"])).first()
        if user:
            check_pwd = security.check_password_hash(user.password, user_data["password"])
            if check_pwd:
                return {"message": "Login successful"}, 200
            return {"message": "Incorrect password"}, 404
        return {"message": "Username does not exist"}, 404
