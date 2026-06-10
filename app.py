from flask import Flask, request, jsonify, g
from database.db import *
from services.user_services import *
from services.task_services import *
from dotenv import load_dotenv
import os
from http import HTTPStatus
from services.config import *
from services.auth import *

ensure_env_file()

load_dotenv()

app = Flask(__name__)

key = os.environ.get("SECRET_KEY")

init_db()


@app.route("/register", methods=["POST"])
def register():

    allowed_fields = {"name", "email", "password"}

    user = request.json
    if not user:
        return jsonify(error="Invalid JSON"), HTTPStatus.BAD_REQUEST

    incoming_fields = set(user.keys())

    extra = incoming_fields - allowed_fields
    if extra:
        return jsonify(error="Unexpected fields in request"), HTTPStatus.BAD_REQUEST

    missing = allowed_fields - incoming_fields
    if missing:
        return jsonify(error="Missing fields in request"), HTTPStatus.BAD_REQUEST

    email = str(user.get("email")).strip().lower()
    password = str(user.get("password")).strip()
    name = str(user.get("name")).strip()

    validate = validate_email(email)
    if not validate:
        return jsonify(error="Please enter a valid email"), HTTPStatus.BAD_REQUEST
    result, message = register_user(name, email, password)

    if message == "existing":
        return jsonify(error="Email exists"), HTTPStatus.CONFLICT

    if result:
        return jsonify(success=f"{result}"), HTTPStatus.CREATED

    return jsonify(error="Unexpected error"), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/login", methods=["POST"])
def login():
    allowed_fields = {"email", "password"}
    user = request.json

    if not user:
        return jsonify(error="Invalid JSON"), HTTPStatus.BAD_REQUEST

    incoming_fields = set(user.keys())

    missing = allowed_fields - incoming_fields
    if missing:
        return jsonify(error="Missing fields in request"), HTTPStatus.BAD_REQUEST

    extra = incoming_fields - allowed_fields
    if extra:
        return jsonify(error="Extra fields in request"), HTTPStatus.BAD_REQUEST

    email = str(user.get("email")).strip().lower()
    password = str(user.get("password")).strip()

    validate = validate_email(email)
    if not validate:
        return jsonify(error="Please enter a valid email"), HTTPStatus.BAD_REQUEST

    token, error = login_user(email, password)
    if error:
        return jsonify(error=f"{error}"), HTTPStatus.UNAUTHORIZED

    return jsonify(success=f"{token}"), HTTPStatus.OK


@app.route("/tasks", methods=["GET"])
@login_required
def tasks():
    token = request.headers.get("Authorization")

    user_id = get_user_id(token)

    tasks, error = all_tasks(user_id)

    if not user_id:
        return jsonify(error="Valid token required"), HTTPStatus.UNAUTHORIZED

    if error:
        return jsonify(error="No tasks found"), HTTPStatus.NOT_FOUND

    return jsonify([dict(row) for row in tasks]), HTTPStatus.OK


@app.route("/add-tasks", methods=["POST"])
@login_required
def add_tasks():
    allowed_fields = {"title", "description", "status"}

    header = request.headers.get("Authorization")

    user_id = get_user_id(header)

    task = request.json

    if not task:
        return jsonify(error="Please include a task"), HTTPStatus.BAD_REQUEST

    incoming_fields = set(task.keys())

    missing = allowed_fields - incoming_fields
    if missing:
        return jsonify(error="Missing fields in request"), HTTPStatus.BAD_REQUEST

    extra = incoming_fields - allowed_fields
    if extra:
        return jsonify(error="Extra fields in request"), HTTPStatus.BAD_REQUEST

    task, error = add_task(task, user_id)
    if error:
        return jsonify(error=f"{error}"), HTTPStatus.NOT_ACCEPTABLE

    return jsonify(task), HTTPStatus.CREATED


@app.route("/task/<int:_id>", methods=["DELETE"])
@login_required
def delete_tasks(_id):
    header = request.headers.get("Authorization")

    user_id = get_user_id(header)

    error = delete_task(user_id, _id)

    if error == "no task":
        return jsonify(error="No task found"), HTTPStatus.NOT_FOUND

    if error == "deleted":
        return jsonify(success="Task deleted"), HTTPStatus.NO_CONTENT

    if error == "error":
        return jsonify(error="Unable to delete"), HTTPStatus.BAD_REQUEST


@app.route("/task/<int:_id>", methods=["PUT"])
@login_required
def update_tasks(_id):
    allowed_fields = {"title", "description", "status"}

    header = request.headers.get("Authorization")

    user_id = get_user_id(header)

    fields = request.json

    for field in fields.keys():
        if field not in allowed_fields:
            return jsonify(error="Invalid fields"), HTTPStatus.BAD_REQUEST

    for key, value in fields.items():
        error = update_task(_id, key, value, user_id)
        if error:
            return jsonify(error="Unable to update task"), HTTPStatus.BAD_REQUEST

    return jsonify(success="updated"), HTTPStatus.OK


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port, host="0.0.0.0")
