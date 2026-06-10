from flask import request
import os
from dotenv import load_dotenv
from database.db import *

load_dotenv()

key = os.environ.get("SECRET_KEY")


def all_tasks(user_id):
    tasks = execute(
        """
            select * from tasks where user_id = ?;
            """,
        (user_id,),
    )
    
    if tasks:
        tasks = list(tasks)
        
    if not tasks:
        return None, "No tasks"
    
    return tasks, None


def add_task(task, user_id):
    try:
        execute(
        """
            insert into tasks (user_id, title, description) values (?, ?, ?);
            """,
        (
            user_id,
            task["title"],
            task["description"],
        ),
    )
        return "success"
    except:
        return None
    
