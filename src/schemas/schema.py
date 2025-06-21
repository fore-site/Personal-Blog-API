from marshmallow import fields, Schema, validate
from models import Post
    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    createdAt = fields.DateTime(dump_only=True)
    posts = fields.List(fields.Nested(lambda: PostSchema(only=("id", "title", "content"))), dump_only=True)
    comments = fields.List(fields.Nested(lambda: CommentSchema(only=("content", "post"))), dump_only=True)

class PostSchema(Schema):
    class Meta():
        model = Post

    id = fields.Int(dump_only=True)
    category = fields.Str(required=True)
    content = fields.Str(required=True)
    tags = fields.Str(required=True)
    title = fields.Str(required=True)
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)
    user_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(UserSchema, only=("id","username"), dump_only=True)
    comments = fields.List(fields.Nested(lambda: CommentSchema(only=("content", "user"))), dump_only=True)
    comment_count = fields.Int(dump_only=True)

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    postedAt = fields.DateTime(dump_only=True)
    editedAt = fields.DateTime(dump_only=True)
    user_id = fields.Int(required=True, load_only=True)
    post_id = fields.Int(required=True, load_only=True)
    post = fields.Nested(PostSchema, only=("id", "title", "content"), dump_only=True)
    user = fields.Nested(UserSchema, only=("id", "username"), dump_only=True)

class PostUpdateSchema(Schema):
    category = fields.Str()
    tags = fields.List(fields.Str())
    content = fields.Str()
    title = fields.Str()
    updatedAt = fields.DateTime(dump_only=True)

class PostPutSchema(Schema):
    category = fields.Str(required=True)
    tags = fields.List(fields.Str(required=True))
    content = fields.Str(required=True)
    title = fields.Str(required=True)
    updatedAt = fields.DateTime(dump_only=True)

class PostQuerySchema(Schema):
    tags = fields.Str()
    term = fields.Str()
