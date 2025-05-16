import marshmallow as ma

class PostSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    category = ma.fields.Str(required=True)
    content = ma.fields.Str(required=True)
    tags = ma.fields.List(ma.fields.Str(required=True))
    title = ma.fields.Str(required=True)
    createdAt = ma.fields.DateTime(dump_only=True)
    updatedAt = ma.fields.DateTime(dump_only=True)

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