from utils.blocklist import jwt_redis_blocklist, ACCESS_EXPIRES
from middlewares.authMiddleware import user_is_active
from datetime import datetime
from flask import jsonify
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from models import User
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from config.extensions import db
from models.schema import UserSchema, UserLoginSchema, UserUpdateSchema
from werkzeug import security

blp = Blueprint("user", __name__, description="Operation on User")

@blp.route("/register")
class UserRoute(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):    
        user_data.update({"createdAt": datetime.now(), "password": security.generate_password_hash(user_data["password"], "scrypt", 8)})
        if user_data["id"] == 1:
            user_data["role"] = "admin"
        try:
            db.session.execute(insert(User).values(user_data))
        except IntegrityError as e:
            db.session.rollback()
            error = str(e.__dict__["orig"])
            if "users.email" in error:
                abort(409, message="email already exists.")
            else:
                abort(409, message="username already existss")
        db.session.commit()
        return user_data

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = db.session.scalars(select(User).where(User.username == user_data["username"])).first()
        if user and security.check_password_hash(user.password, user_data["password"]):
            if not user.is_active:
                abort(403, message="Account deactivated.")
            else:
                access_token = create_access_token(identity=str(user.id))
                refresh_token = create_refresh_token(identity=str(user.id))
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
        abort(401, message="Invalid username or password")


@blp.route("/users/<int:id>")
class FindUserRoute(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self, id):
        searched_user = db.session.scalars(select(User).where(User.id == id)).all()
        if searched_user:
            return searched_user
        else:
            abort(404, message="User not found")

@blp.route("/profile")
class CurrentUserRoute(MethodView):
    @user_is_active
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self):
        current_user = get_jwt_identity()
        user = db.session.scalars(select(User).where(User.id == int(current_user))).first()
        return user
    
    @user_is_active
    @jwt_required()
    @blp.arguments(UserUpdateSchema)
    def patch(self, user_body):
        current_user = get_jwt_identity()
        user = db.session.scalars(select(User).where(User.id == int(current_user))).first()
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
                abort(409, message=("Username already exists"))
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
                        abort(409, message="email already exists.")
                db.session.commit()
                return {"message": f"{credential} successfully updated"}, 200
            else:
                abort(401, message="Current password is incorrect.")

    @user_is_active
    @jwt_required(verify_type=False)
    def delete(self):
        current_user = get_jwt_identity()
        db.session.execute(delete(User).where(User.id == int(current_user)))
        db.session.commit()

        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        return jsonify({"message": f"User successfully deleted. {ttype.capitalize()} token revoked."}), 204

@blp.route("/logout")
class UserLogout(MethodView):
    @user_is_active
    @jwt_required(verify_type=False)
    def post(self):
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        return jsonify({"message": f"Successfully logged out. {ttype.capitalize()} token revoked"}), 200
    
@blp.route("/refresh")
class RefreshToken(MethodView):
    @user_is_active
    @jwt_required(refresh=True)
    def post(self):
        access_token = create_access_token(identity=get_jwt_identity())
        return jsonify({"access_token": access_token}), 200