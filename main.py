from fastapi import FastAPI
from app.routes import router  # Import router from the app folder

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Smart ToDo API is running!"}

