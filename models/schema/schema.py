import datetime

from pydantic import BaseModel

class CommentBase(BaseModel):
    text: str
    date_from: datetime.date

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    post_id: int
    author_id: int

    class Config:
        env_file = ".env"


class PostBase(BaseModel):
    title: str
    description: str
    date_from: datetime.date
    date_to: datetime.date

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    author_id:int
    comments: list[Comment] = []

    class Config:
        env_file = ".env"

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    posts: list[Post] = []
    comments: list[Comment] = []

    class Config:
        env_file = ".env"
