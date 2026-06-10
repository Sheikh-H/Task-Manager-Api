from flask import request, jsonify
import os
from dotenv import load_dotenv
from database.db import *

load_dotenv()

key = os.environ.get("SECRET_KEY")


def all_tasks(user_id, limit, offset):
    total = fetch_one(
        """select count(*) as count from tasks where user_id = ?;""", (int(user_id),)
    )["count"]
    
    
    tasks = fetch_many(
        """
            select * from tasks 
            where user_id = ?
            limit ?
            offset ?;
            """,
        (int(user_id), limit, offset),
    )

    if tasks:
        tasks = list(tasks)
        return tasks, total


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
    _id = int(_id)
    user_id = int(user_id)
    try:
        task = fetch_one(
            """
            select * from tasks 
            where user_id = ? and id = ?;
            """,
            (
                user_id,
                _id,
            ),
        )

        if not task:
            return "error"

        if key == "title":
            execute(
                """
                update tasks 
                set title = ? 
                where id = ? and user_id = ?;
                """,
                (
                    value,
                    _id,
                    user_id,
                ),
            )
        if key == "description":
            execute(
                """
                update tasks 
                set description = ? 
                where id = ? and user_id = ?;
                """,
                (
                    value,
                    _id,
                    user_id,
                ),
            )

        if key == "status":
            execute(
                """
                update tasks 
                set status = ? 
                where id = ? and user_id = ?;
                """,
                (
                    value,
                    _id,
                    user_id,
                ),
            )
        return None
    except:
        return "error"
