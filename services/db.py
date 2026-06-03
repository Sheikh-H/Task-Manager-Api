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
    # id - custom field
    # name
    # email
    # password
    # createdAt
    # updatedAt
    
def login_user(user):
    # email
    # password
    # if auth, token
    # else error

def add_task(task):
    # user_id
    # task title
    # task_status
    # task_due
    # descriptipn
    # createdAt
    # updatedAt
    