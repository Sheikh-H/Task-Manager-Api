from flask import request, jsonify
import os
from dotenv import load_dotenv
from database.db import *

load_dotenv()

key = os.environ.get("SECRET_KEY")


def all_tasks(user_id):
    tasks = fetch_many(
        """
            select * from tasks where user_id = ?;
            """,
        (int(user_id),),
    )

    if tasks:
        tasks = list(tasks)
        return tasks, None

    if not tasks:
        return None, "No tasks"


def add_task(task, user_id):
    try:
        execute(
            """
            insert into tasks (user_id, title, description) values (?, ?, ?);
            """,
            (
                int(user_id),
                task["title"],
                task["description"],
            ),
        )
        return task, None
    except Exception as e:
        return None, f"{e}"


def delete_task(user_id, _id):
    try:
        task = fetch_one(
            """ select * from tasks where user_id = ? and id = ?;""",
            (
                user_id,
                _id,
            ),
        )
        if not task:
            return "no task"
        execute(
            """
                delete from tasks where user_id = ? and id = ?;""",
            (
                user_id,
                _id,
            ),
        )
        return "deleted"
    except:
        return "error"


def update_task(_id, key, value, user_id):
    try:
        task = fetch_one(
            """select * from tasks where user_id = ? and id = ?;"""(
                user_id,
                _id,
            )
        )

        if not task:
            return "error"

        execute(
            """update tasks set ? = ? where id = ? and user_id = ?"""(
                key,
                value,
                _id,
                user_id,
            )
        )

        return None
    except:
        return "error"
