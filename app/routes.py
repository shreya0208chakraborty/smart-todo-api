from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import user_collection, task_collection
from app.models import User, Task
from app.auth import hash_password, verify_password, create_access_token, decode_token
from bson import ObjectId

router = APIRouter()
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return payload["username"]

@router.post("/register")
def register(user: User):
    if user_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="User exists")
    user.password = hash_password(user.password)
    user_collection.insert_one(user.dict())
    return {"message": "User registered"}

@router.post("/login")
def login(user: User):
    db_user = user_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"username": user.username})
    return {"access_token": token}

@router.post("/tasks")
def create_task(task: Task, username: str = Depends(get_current_user)):
    task_dict = task.dict()
    task_dict["username"] = username
    task_collection.insert_one(task_dict)
    return {"message": "Task created"}

@router.get("/tasks")
def get_tasks(username: str = Depends(get_current_user)):
    tasks = []
    for task in task_collection.find({"username": username}):
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return tasks

@router.put("/tasks/{task_id}")
def update_task(task_id: str, task: Task, username: str = Depends(get_current_user)):
    task_collection.update_one(
        {"_id": ObjectId(task_id), "username": username},
        {"$set": task.dict()}
    )
    return {"message": "Task updated"}

@router.delete("/tasks/{task_id}")
def delete_task(task_id: str, username: str = Depends(get_current_user)):
    task_collection.delete_one({"_id": ObjectId(task_id), "username": username})
    return {"message": "Task deleted"}
