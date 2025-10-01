from flask import jsonify
from flask_smorest import abort
from sqlalchemy import select, insert, update, delete
from config.extensions import db
from models import Tag

def get_tags(pagination_parameters):
    limit = pagination_parameters.page_size
    offset = pagination_parameters.first_item
    all_tags = db.session.scalars(select(Tag)
                                  .limit(limit)
                                  .offset(offset)).all()
    pagination_parameters.item_count = len(all_tags)
    return all_tags

def get_single_tag(tag_id):
    tag = db.session.scalars(select(Tag).where(Tag.id == tag_id)).first()
    if tag:
        return tag
    else:
        abort(404, message="Tag not found.")

# ADMIN ACTIONS

def create_tag(tag_data):
    db.session.execute(insert(Tag), [tag_data])
    db.session.commit()
    return tag_data

def edit_tag(tag_data, tag_id):
    tag = select(Tag).where(Tag.id == tag_id)
    if tag:
        db.session.execute(update(Tag), [{"id": tag_id, "name": tag_data["name"]}])
        db.session.commit()
        return jsonify({"message": "Tag updated"}), 200
    else:
        abort(404, message="Tag not found.")

def delete_tag(tag_id):
    tag = db.get_or_404(Tag, tag_id)
    if not tag.posts:
        db.session.execute(delete(Tag).where(Tag.id == tag_id))
        db.session.commit()
        return {"message": "Tag deleted."}
    else:
        abort(400, message="There are posts associated with this tag. Tag cannot be deleted.")

