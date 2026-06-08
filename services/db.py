import pymongo
import os
from dotenv import load_dotenv
import json
import secrets


load_dotenv()


client = pymongo.MongoClient(os.environ.get("MONGO_URI"))
database = client["rdmpsh-todo"]
tasks_table = database["todo-list"]
users_table = database['user_logins']

def register_user(user):
    