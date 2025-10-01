from flask_smorest import abort, Blueprint
from sqlalchemy import select
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