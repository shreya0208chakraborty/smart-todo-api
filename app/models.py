from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
