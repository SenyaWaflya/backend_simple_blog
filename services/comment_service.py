from sqlalchemy.orm import Session

from models import models
from models.schema import schema

def get_all_comments_by_post_id(db: Session, post_id: int, offset: int = 0, limit: int = 100):
    return db.query(models.Comment).offset(offset).limit(limit).filter(models.Comment.post_id == post_id)

def create_comment_to_post(db: Session, comment_creation: schema.CommentCreate, post_id: int, user_id: int):
    db_comment = models.Comment(**comment_creation.dict(), post_id=post_id, author_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment