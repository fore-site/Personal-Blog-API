from flask_smorest import abort, Blueprint
from sqlalchemy import select
from config.extensions import db
from models import Tag


def get_tags():
    all_tags = db.session.scalar(select(Tag)).all()
    return all_tags

def get_single_tag(tag_id):
    tag = db.session.scalar(select(Tag).where(Tag.id == tag_id)).first()
    if tag:
        return tag
    else:
        abort(404, message="Tag not found.")