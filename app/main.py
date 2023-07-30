from fastapi import FastAPI, HTTPException, Request
from .models import MovieComment
from .service_methods import MovieCommentManager
from typing import List


app = FastAPI()



comment_manager = MovieCommentManager()


#route to post comment for any specific user
@app.post("/comments/", response_model=MovieComment)
async def create_comment(request: Request):
    comment_data = await request.json()
    
    # Manually convert the users and users_who_commented lists to sets
    comment_data["users"] = set(comment_data["users"])
    comment_data["users_who_commented"] = set(comment_data["users_who_commented"])
    
    comment = MovieComment(**comment_data)
    comment_manager.create_comment(comment)
    return comment


#route to fetch the comments on any specific movie_id
@app.get("/comments/{movie_id}", response_model=List[MovieComment])
async def comments_by_movie_id(movie_id: str):
    comments = comment_manager.get_comments_by_movie_id(movie_id)
    if not comments:
        raise HTTPException(status_code=404, detail="Movie comments not found")
    return comments



#route to fetch details on any movie_id with specific users
@app.get("/user_comments/{movie_id}/{user}", response_model=List[MovieComment])
async def comments_for_user(movie_id: str, user: str):
    user_comments = comment_manager.get_comments_for_user(movie_id, user)
    if not user_comments:
        raise HTTPException(status_code=404, detail="User comments not found")
    return user_comments



