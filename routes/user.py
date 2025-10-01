from middlewares.authMiddleware import user_is_active, admin_only
from flask.views import MethodView
from flask_smorest import  Blueprint
from flask_jwt_extended import jwt_required
from models.schema import UserSchema, UserLoginSchema, UserUpdateSchema
from controllers.user import login_user, register_user, get_user,get_all_users , get_profile, update_profile, deactivate_user, logout_user, refresh_token, suspend_user, restore_user

blp = Blueprint("user", __name__, description="Operation on User")

@blp.route("/register")
class UserRoute(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):    
        return register_user(user_data)
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        return login_user(user_data)

@blp.route("/users/<int:id>")
class FindUserRoute(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self, id):
        return get_user(id)

@blp.route("/profile")
class CurrentUserRoute(MethodView):
    @jwt_required()
    @user_is_active
    @blp.response(200, UserSchema)
    def get(self):
        return get_profile()
    
    @jwt_required()
    @user_is_active
    @blp.arguments(UserUpdateSchema)
    def patch(self, user_body):
        return update_profile(user_body)

    @jwt_required(verify_type=False)
    @user_is_active
    def delete(self):
        return deactivate_user
    
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required(verify_type=False)
    @user_is_active
    def post(self):
        return logout_user()
    
@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    @user_is_active
    def post(self):
        return refresh_token()
    
 # ADMIN ACTIONS
 #    
@blp.route("/users")
class AllUsersRoute(MethodView):
    @jwt_required()
    @admin_only
    @user_is_active
    @blp.response(200, UserSchema(many=True))
    @blp.paginate()
    def get(self, pagination_parameters):
        return get_all_users(pagination_parameters)
    
@blp.route("/users/<int:user_id>/suspend")
class AdminUserRoute(MethodView):
    @jwt_required(verify_type=False)
    @admin_only
    @user_is_active
    def patch(self, user_id):
        return suspend_user(user_id)
        
@blp.route("/admin/users/<int:user_id>/restore")
class AdminRestoreUser(MethodView):
    @jwt_required()
    @admin_only
    @user_is_active
    def patch(self, user_id):
        return restore_user(user_id)