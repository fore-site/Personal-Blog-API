from marshmallow import fields, Schema, validate, validates_schema, ValidationError
from models import Post
    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=4, max=10))
    email = fields.Email(required=True, validate=validate.Email(error="Enter a valid email address"))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=9, max=20))
    createdAt = fields.DateTime(dump_only=True)
    posts = fields.List(fields.Nested(lambda: PostSchema(only=("id", "title", "content"))), dump_only=True)
    comments = fields.List(fields.Nested(lambda: CommentSchema(only=("id", "content", "post"))), dump_only=True)
    role = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)

class UserLoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=4, max=10))
    password = fields.Str(required=True, validate=validate.Length(min=9, max=20))

class UserUpdateSchema(Schema):
    username = fields.Str(validate=validate.Length(min=4, max=10))
    current_password = fields.Str(load_only=True, validate=validate.Length(min=9, max=20))
    new_password = fields.Str(load_only=True, validate=validate.Length(min=9, max=20))
    confirm_new_password = fields.Str(load_only=True, validate=validate.Length(min=9, max=20))
    email = fields.Email(validate=validate.Email(error="Enter a valid email address"))
    
    @validates_schema
    def validate_password(self, data, **kwargs):
        if data.get("new_password") and not data.get("current_password"):
            raise ValidationError(message="Must enter old password.")
        if data.get("email") and not data.get("current_password"):
            raise  ValidationError(message="Must enter current password.")

class PostSchema(Schema):
    class Meta():
        model = Post
        exclude = ("comments", "user_id")

    id = fields.Int(dump_only=True)
    content = fields.Str(required=True, validate=validate.Length(min=1))
    title = fields.Str(required=True, validate=validate.Length(min=1))
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
    user = fields.Nested(UserSchema, only=("id", "username"), dump_only=True)
    comments = fields.List(fields.Nested(lambda: CommentSchema(only=("id", "content", "user"))), dump_only=True)
    comment_count = fields.Int(dump_only=True)
    tags = fields.List(fields.Nested(lambda: TagSchema(only=("id", "name"))), dump_only=True)

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True, validate=validate.Length(min=1))
    postedAt = fields.DateTime(dump_only=True)
    editedAt = fields.DateTime(dump_only=True)
    post = fields.Nested(PostSchema, only=("id", "title", "content"), dump_only=True)
    user = fields.Nested(UserSchema, only=("id", "username"), dump_only=True)

class PostUpdateSchema(Schema):
    content = fields.Str(validate=validate.Length(min=1))
    title = fields.Str(validate=validate.Length(min=1))
    updatedAt = fields.DateTime(dump_only=True)

class PostQuerySchema(Schema):
    tags = fields.Str()
    q = fields.Str()

class TagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    posts = fields.List(fields.Nested(lambda: PostSchema(only=("id", "title", "content"))), dump_only=True)