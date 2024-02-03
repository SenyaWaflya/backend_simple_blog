import uvicorn

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from models import database #Base, SessionLocal, engine
from models import schema
from services.user_service import get_user_by_email, create_user, get_user
from services.post_service import get_post, get_all, get_all_by_author_id, create_post
from services.comment_service import get_all_comments_by_post_id, create_comment_to_post

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def get_docs_endpoint(request: Request):
    return RedirectResponse(f'{request.url}docs')

@app.post("/users/", response_model=schema.schema.User)
async def create_user_endpoint(user: schema.schema.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schema.schema.User)
async def read_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/{user_id}/posts", response_model=list[schema.schema.Post])
async def get_all_posts_for_author_endpoint(user_id: int, db: Session = Depends(get_db)):
    posts = get_all_by_author_id(db, user_id)
    if posts is None:
        raise HTTPException(status_code=404, detail="Posts for author not found")
    return posts

@app.get("/posts/", response_model=list[schema.schema.Post])
async def get_posts_endpoint(db: Session = Depends(get_db)):
    db_posts = get_all(db)
    if db_posts is None:
        raise HTTPException(status_code=404, detail="Posts not found")
    return db_posts

@app.get("/posts/{post_id}", response_model=schema.schema.Post)
async def get_post_by_id_endpoint(post_id: int, db: Session = Depends(get_db)):
    post = get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/post/{user_id}", response_model=schema.schema.Post)
async def create_post_endpoint(user_id: int, post: schema.schema.PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post, user_id)

@app.get("/posts/{post_id}/comments", response_model=list[schema.schema.Comment])
async def get_comments_to_post_endpoint(post_id: int, db: Session = Depends(get_db)):
    post_comments = get_all_comments_by_post_id(db, post_id)
    if post_comments is None:
        raise HTTPException(status_code=404, detail="Comments not found")
    return post_comments

@app.post("/post/{post_id}/comment", response_model=schema.schema.Comment)
async def create_comment_endpoint(post_id: int, user_id: int, comment: schema.schema.CommentCreate, db: Session = Depends(get_db)):
    return create_comment_to_post(db, comment, post_id, user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)