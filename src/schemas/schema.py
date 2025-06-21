import marshmallow as ma
from models import Post
    
class UserSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    username = ma.fields.Str(required=True)
    email = ma.fields.Str(required=True)
    password = ma.fields.Str(required=True, load_only=True)
    createdAt = ma.fields.DateTime(dump_only=True)
    posts = ma.fields.List(ma.fields.Nested(lambda: PostSchema(only=("id", "title", "content"))), dump_only=True)
    comments = ma.fields.List(ma.fields.Nested(lambda: CommentSchema(only=("content", "post"))), dump_only=True)

class PostSchema(ma.Schema):
    class Meta():
        model = Post

    id = ma.fields.Int(dump_only=True)
    category = ma.fields.Str(required=True)
    content = ma.fields.Str(required=True)
    tags = ma.fields.Str(required=True)
    title = ma.fields.Str(required=True)
    createdAt = ma.fields.DateTime(dump_only=True)
    updatedAt = ma.fields.DateTime(dump_only=True)
    user_id = ma.fields.Int(required=True, load_only=True)
    user = ma.fields.Nested(UserSchema, only=("id","username"), dump_only=True)
    comments = ma.fields.List(ma.fields.Nested(lambda: CommentSchema(only=("content", "user"))), dump_only=True)
    comment_count = ma.fields.Int(dump_only=True)

class CommentSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    content = ma.fields.Str(required=True)
    postedAt = ma.fields.DateTime(dump_only=True)
    editedAt = ma.fields.DateTime(dump_only=True)
    user_id = ma.fields.Int(required=True, load_only=True)
    post_id = ma.fields.Int(required=True, load_only=True)
    post = ma.fields.Nested(PostSchema, only=("id", "title", "content"), dump_only=True)
    user = ma.fields.Nested(UserSchema, only=("id", "username"), dump_only=True)

class PostUpdateSchema(ma.Schema):
    category = ma.fields.Str()
    tags = ma.fields.List(ma.fields.Str())
    content = ma.fields.Str()
    title = ma.fields.Str()
    updatedAt = ma.fields.DateTime(dump_only=True)

class PostPutSchema(ma.Schema):
    category = ma.fields.Str(required=True)
    tags = ma.fields.List(ma.fields.Str(required=True))
    content = ma.fields.Str(required=True)
    title = ma.fields.Str(required=True)
    updatedAt = ma.fields.DateTime(dump_only=True)

class PostQuerySchema(ma.Schema):
    tags = ma.fields.Str()
    term = ma.fields.Str()
