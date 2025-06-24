from marshmallow import fields, Schema, validate
from models import Post
    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=4, max=10))
    email = fields.Str(required=True, validate=validate.Email(error="Enter a valid email address"))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=9, max=20))
    createdAt = fields.DateTime(dump_only=True)
    posts = fields.List(fields.Nested(lambda: PostSchema(only=("id", "title", "content"))), dump_only=True)
    comments = fields.List(fields.Nested(lambda: CommentSchema(only=("content", "post"))), dump_only=True)

class PostSchema(Schema):
    class Meta():
        model = Post
        exclude = ("comments",)

    id = fields.Int(dump_only=True)
    content = fields.Str(required=True, validate=validate.Length(min=1))
    tags = fields.Str(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)
    user_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(UserSchema, only=("id","username"), dump_only=True)
    comments = fields.List(fields.Nested(lambda: CommentSchema(only=("content", "user"))), dump_only=True)
    comment_count = fields.Int(dump_only=True)

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True, validate=validate.Length(min=1))
    postedAt = fields.DateTime(dump_only=True)
    editedAt = fields.DateTime(dump_only=True)
    user_id = fields.Int(required=True, load_only=True)
    post_id = fields.Int(required=True, load_only=True)
    post = fields.Nested(PostSchema, only=("id", "title", "content"), dump_only=True)
    user = fields.Nested(UserSchema, only=("id", "username"), dump_only=True)

class PostUpdateSchema(Schema):
    tags = fields.Str()
    content = fields.Str(validate=validate.Length(min=1))
    title = fields.Str(validate=validate.Length(min=1))
    updatedAt = fields.DateTime(dump_only=True)

class PostPutSchema(Schema):
    tags = fields.List(fields.Str(required=True))
    content = fields.Str(required=True, validate=validate.Length(min=1))
    title = fields.Str(required=True, validate=validate.Length(min=1))
    updatedAt = fields.DateTime(dump_only=True)

class PostQuerySchema(Schema):
    tags = fields.Str()
    term = fields.Str()
