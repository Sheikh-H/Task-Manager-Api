from flask import request, jsonify
from http import HTTPStatus
import jwt
from functools import wraps
from flask import request
from dotenv import load_dotenv
import os
import re

load_dotenv()

key = os.environ.get("SECRET_KEY")


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify(message="Unauthorised"), HTTPStatus.UNAUTHORIZED

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, key, algorithms=["HS256"])

            request.user_id = payload["user_id"]

        except:
            return jsonify(message="Invalid token"), HTTPStatus.UNAUTHORIZED

        return func(*args, **kwargs)

    return wrapper


def validate_email(email):
    regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    return bool(re.match(regex, email))
