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
    tasks = list(tasks)
    return tasks
