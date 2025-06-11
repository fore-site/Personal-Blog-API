import marshmallow as ma
from models import Post
    
class UserSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    username = ma.fields.Str()
    email = ma.fields.Str()
    password = ma.fields.Str()
    createdAt = ma.fields.DateTime(dump_only=True)
    posts = ma.fields.List(ma.fields.Nested(lambda: PostSchema(only=("id", "title", "content"))), dump_only=True)
    comments = ma.fields.List(ma.fields.Nested(lambda: CommentSchema(only=("content", "post_id"))), dump_only=True)

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
    comments = ma.fields.List(ma.fields.Nested(lambda: CommentSchema()), dump_only=True)
    comment_count = ma.fields.Int()

class CommentSchema(ma.Schema):
    content = ma.fields.Str()
    postedAt = ma.fields.DateTime()
    editedAt = ma.fields.DateTime()
    user_id = ma.fields.Int()
    post_id = ma.fields.Int()
    post = ma.fields.Nested(PostSchema, only=("title", "content", "createdAt", "updatedAt"), dump_only=True)
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
