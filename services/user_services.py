from datetime import datetime, timedelta
from database.db import *
from argon2 import PasswordHasher
import jwt
from flask import request
import os
from dotenv import load_dotenv

load_dotenv()


def register_user(name, email, password):
    now = datetime.now().replace(microsecond=0)

    ph = PasswordHasher().hash(password)

    existing_user = fetch_one("select * from users where email = ?", (email,))
    if existing_user:
        return "existing"

    execute(
        "insert into users (name, email, password_hash, created_at) values (?, ?, ?, ?)",
        (
            name,
            email,
            ph,
            str(now),
        ),
    )
    return None, "registered"


def login_user(email, password):
    user = fetch_one(
        "select id, name, email, password_hash from users where email = ?", (email,)
    )
    try:
        PasswordHasher().verify(user["password_hash"], password)
    except:
        return None, "password incorrect"

    payload = {
        "user_id": str(user["id"]),
    }

    key = os.environ.get("SECRET_KEY")

    token = jwt.encode(payload, key, algorithm="HS256")

    return token, None

