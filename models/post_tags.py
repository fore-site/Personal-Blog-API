from config.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

class PostTags(db.Model):
    __tablename__ = "posts_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))