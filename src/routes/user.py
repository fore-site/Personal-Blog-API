from blocklist import jwt_redis_blocklist, ACCESS_EXPIRES
from datetime import datetime
from flask import jsonify
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity, get_jti
from models import User
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.extensions import db
from src.schemas.schema import UserSchema, UserLoginSchema, UserUpdateSchema, UserPathSchema
from werkzeug import security

blp = Blueprint("user", __name__, description="Operation on User")

@blp.route("/register")
class UserRoute(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):    
        user_data.update({"createdAt": datetime.now(), "password": security.generate_password_hash(user_data["password"], "scrypt", 8)})
        try:
            db.session.execute(insert(User).values(user_data))
        except IntegrityError as e:
            db.session.rollback()
            error = str(e.__dict__["orig"])
            if "users.email" in error:
                abort(403, message="email already exists.")
            else:
                abort(403, message="username already existss")
        db.session.commit()
        return user_data

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = db.session.scalars(select(User).where(User.username == user_data["username"])).first()
        if user and security.check_password_hash(user.password, user_data["password"]):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        abort(401, message="Invalid username or password")

@blp.route("/user/<username>")
class FindUserRoute(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self, username):
        searched_user = db.session.scalars(select(User).where(User.username == username)).all()
        if searched_user:
            return searched_user
        else:
            abort(404, message="User not found")

@blp.route("/user/me")
class CurrentUserRoute(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self):
        current_user = get_jwt_identity()
        user = db.session.scalars(select(User).where(User.id == current_user)).first()
        return user
    
    @jwt_required()
    @blp.arguments(UserUpdateSchema)
    def patch(self, user_body):
        current_user = get_jwt_identity()
        user = db.session.scalars(select(User).where(User.id == current_user)).first()
        if user_body.get("username"):
            if user_body.get("current_password"):
                if security.check_password_hash(user.password, user_body["current_password"]):
                    pass
                else:
                    abort(401, message="Current password is incorrect.")
            try:
                db.session.execute(update(User), [{"id": user.id, "username": user_body["username"]}])
            except IntegrityError as e:
                db.session.rollback()
                abort(403, message=("Username already exists"))
            else:
                db.session.commit()
                return {"message": "Credentials successfully updated."}, 200
        if user_body.get("new_password") or user_body.get("email"):
            if security.check_password_hash(user.password, user_body.get("current_password")):
                credential = ""
                if user_body.get("new_password"):
                    credential = "password"
                    db.session.execute(update(User), [{"id": user.id, "password": security.generate_password_hash(user_body["new_password"], "scrypt", 8)}])
                if user_body.get("email"):
                    credential = "email"
                    try:
                        db.session.execute(update(User), [{"id": user.id, "email": user_body["email"]}])
                    except IntegrityError as e:
                        db.session.rollback()
                        abort(403, message="email already exists.")
                db.session.commit()
                return {"message": f"{credential} successfully updated"}, 200
            else:
                abort(401, message="Current password is incorrect.")

    @jwt_required(verify_type=False)
    def delete(self):
        current_user = get_jwt_identity()
        db.session.execute(delete(User).where(User.id == current_user))
        db.session.commit()

        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        return jsonify({"message": f"User successfully deleted. {ttype.capitalize()} token revoked."}), 204

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required(verify_type=False)
    def post(self):
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        return jsonify({"message": f"Successfully logged out. {ttype.capitalize()} token revoked"}), 200
    
@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        access_token = create_access_token(identity=get_jwt_identity())
        return jsonify({"access_token": access_token}), 200