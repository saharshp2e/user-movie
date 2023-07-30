from pydantic import BaseModel
from typing import Set

class MovieComment(BaseModel):
    movie_id: str
    comments: str
    users: Set[str]
    users_who_commented: Set[str]
