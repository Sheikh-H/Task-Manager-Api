from flask import Flask, request, jsonify
from database.db import *
from services.user_services import *
from dotenv import load_dotenv
import os
from http import HTTPStatus
from services.config import *
from services.auth import *

ensure_env_file()

load_dotenv()

app = Flask(__name__)

init_db()


@app.route("/register", methods=["POST"])
def register():

    allowed_fields = {"name", "email", "password"}

    user = request.json
    if not user:
        return jsonify(message="Invalid JSON"), HTTPStatus.BAD_REQUEST

    incoming_fields = set(user.keys())

    extra = incoming_fields - allowed_fields
    if extra:
        return jsonify(message="Unexpected fields in request"), HTTPStatus.BAD_REQUEST

    missing = allowed_fields - incoming_fields
    if missing:
        return jsonify(message="Missing fields in request"), HTTPStatus.BAD_REQUEST

    result = register_user(
        str(user.get("name")), str(user.get("email")), str(user.get("password"))
    )

    if result == "existing":
        return jsonify(message="Email exists"), HTTPStatus.CONFLICT

    if result == "registered":
        return jsonify(message="Account created, please login"), HTTPStatus.CREATED

    return jsonify(message="Unexpected error"), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/login", methods=["POST"])
def login():
    allowed_fields = {"email", "password"}
    user = request.json

    if not user:
        return jsonify(message="Invalid JSON"), HTTPStatus.BAD_REQUEST

    incoming_fields = set(user.keys())

    missing = allowed_fields - incoming_fields
    if missing:
        return jsonify(message="Missing fields in request"), HTTPStatus.BAD_REQUEST

    extra = incoming_fields - allowed_fields
    if extra:
        return jsonify(message="Extra fields in request"), HTTPStatus.BAD_REQUEST

    token, error = login_user(user.get("email"), user.get("password"))
    if error:
        return jsonify(error), HTTPStatus.UNAUTHORIZED

    return jsonify(token), HTTPStatus.OK


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port, host="0.0.0.0")
