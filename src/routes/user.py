from blocklist import jwt_redis_blocklist, ACCESS_EXPIRES
from datetime import datetime
from flask import jsonify
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from models import User
from sqlalchemy import select, update, insert, delete
from src.extensions import db
from src.schemas.schema import UserSchema, UserLoginSchema, UserUpdateSchema
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

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = db.session.scalars(select(User).where(User.username == user_data["username"])).first()
        if user and security.check_password_hash(user.password, user_data["password"]):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        abort(401, message="Invalid username or password")

@blp.route("/user/<int:user_id>")
class UserIDRoute(MethodView):
    def get(self, user_id):
        single_user = db.session.execute(select(User).where(User.id == user_id)).all()
        user_schema = UserSchema(many=True)
        result = user_schema.dump(single_user)
        return result, 200

    @jwt_required()
    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserUpdateSchema)
    def patch(self, user_body, user_id):
        user = db.session.scalars(select(User).where(User.id == user_id)).first()
        if user_body["username"]:
            if user_body["current_password"]:
                if security.check_password_hash(user.password, user_body["current_password"]):
                    pass
                abort(401, message="Current password is incorrect")
            db.session.execute(update(User), [{"id": user_id, "username": user_body["username"]}])
            db.session.commit()
        if user_body["new_password"] or user_body["email"]:
            if security.check_password_hash(user.password, user_body["current_password"]):
                if user_body["new_password"]:
                    db.session.execute(update(User), [{"id": user_id, "password": security.generate_password_hash(user_body["new_password"], "scrypt", 8)}])
                if user_body["email"]:
                    db.session.execute(update(User), [{"id": user_id, "email": user_body["email"]}])
                db.session.commit()
            abort (401, message="Current password is incorrect.")
        return {"message": "Credentials successfully updated."}, 200

    @jwt_required()
    def delete(self, user_id):
        user = db.session.execute(select(User).where(User.id == user_id)).all()
        if not user:
            abort(404, message="User does not exist.")
        db.session.execute(delete(User).where(User.id == user_id))
        db.session.commit()
        return "Okay", 204

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        return jsonify({"message": "Successfully logged out"})
    
@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        access_token = create_access_token(identity=get_jwt_identity())
        return {"access_token": access_token}, 200