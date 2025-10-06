from utils.blocklist import jwt_redis_blocklist, ACCESS_EXPIRES
from datetime import datetime
from flask import jsonify
from flask_smorest import abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity
from models import User
from sqlalchemy import insert, select, update, delete, func
from sqlalchemy.exc import IntegrityError
from config.extensions import db
from werkzeug import security


def login_user(user_data):
    user = db.session.scalars(select(User).where(User.username == user_data["username"])).first()
    if user and security.check_password_hash(user.password, user_data["password"]):
        if user.status == "disabled":
            abort(403, message="Account suspended.")
        else:
            if user.status == "inactive":
                db.session.execute(update(User),[{"id": user.id, "status": "active"}])
                db.session.commit()
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
    abort(401, message="Invalid username or password")

def register_user(user_data):    
    user_data.update({"createdAt": datetime.now(), "password": security.generate_password_hash(user_data["password"], "scrypt", 8)})
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

def get_user(id):
    searched_user = db.session.scalars(select(User).where(User.id == id)).all()
    if searched_user:
        return searched_user
    else:
        abort(404, message="User not found")

def get_profile():
    current_user = get_jwt_identity()
    user = db.session.scalars(select(User).where(User.id == int(current_user))).first()
    return user

def update_profile(user_body):
    current_user = get_jwt_identity()
    user = db.session.scalars(select(User).where(User.id == int(current_user))).first()
    if user_body.get("imageUrl"):
        db.session.execute(update(User), [{"id": user.id, "imageUrl": user_body.get("imageUrl")}])
        db.session.commit()
        return {"message": "Profile photo updated."}, 200
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

def delete_profile_picture():
    current_user = get_jwt_identity()
    db.session.execute(update(User), [{"id": int(current_user), "imageUrl": None}])
    db.session.commit()

def deactivate_user():
    current_user = get_jwt_identity()
    db.session.execute(update(User), [{"id": int(current_user), "status": "inactive"}])
    db.session.commit()

    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify({"message": f"Account successfully deactivated. {ttype.capitalize()} token revoked."}), 202

def logout_user():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify({"message": f"Successfully logged out. {ttype.capitalize()} token revoked"}), 200

def refresh_token():
    access_token = create_access_token(identity=get_jwt_identity())
    return jsonify({"access_token": access_token}), 200

# ADMIN ACTIONS

def get_all_users(pagination_parameters):
    pagination_parameters.item_count = db.session.scalar(select(func.count()).select_from(User))
    limit = pagination_parameters.page_size
    offset = pagination_parameters.first_item
    users = db.session.scalars(select(User)
                               .limit(limit)
                               .offset(offset)).all()
    return users

def suspend_user(user_id):
    user = db.session.scalars(select(User).where(User.id == user_id)).first()
    if not user:
        abort(404, message="User not found.")
    elif user.status == "inactive" or user.status == "disabled":
        abort(409, message="User already deactivated.")
    elif int(get_jwt_identity()) == user_id:
        abort(403, message="Cannot suspend one's self.")
    else:
        db.session.execute(update(User), [{"id": user_id, "status": "disabled"}])
        db.session.commit()
        return jsonify({"message": f"User {user.username} successfully deactivated."}), 202
    
def restore_user(user_id):
    user = db.session.scalars(select(User).where(User.id == user_id)).first()
    if not user:
        abort(404, message="User not found")
    elif user.status == "active":
        abort(409, message="Account already restored")
    else:
        db.session.execute(update(User), [{"id": user_id, "status": "active"}])
        db.session.commit()
        return jsonify({"message": f"User {user.username} successfully restored"}), 200