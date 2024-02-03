from sqlalchemy.orm import Session

from models import models
from models.schema import schema

def get_post(db: Session, post_id):
    return db.query(models.Post).filter(models.Post.id == post_id).first

def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_all_by_author_id(db: Session, author_id, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).filter(models.Post.author_id == author_id).all()

def create_post(db: Session, post_creation: schema.PostCreate, user_id: int):
    db_post = models.Post(**post_creation.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post