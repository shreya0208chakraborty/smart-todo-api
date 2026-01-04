from pymongo import MongoClient

MONGO_URL = "mongodb+srv://shreya:mypassword123@cluster0.chg1qk0.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URL)
db = client["smart_todo_db"]

user_collection = db["users"]
task_collection = db["tasks"]
