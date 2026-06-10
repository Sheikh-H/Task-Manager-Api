from datetime import datetime, timedelta, timezone
from database.db import *
from argon2 import PasswordHasher
import jwt
from flask import request
import os
from dotenv import load_dotenv

load_dotenv()

key = os.environ.get("SECRET_KEY")


def register_user(name, email, password):
    now = datetime.now().replace(microsecond=0)

    ph = PasswordHasher().hash(password)

    existing_user = fetch_one("select * from users where email = ?", (email,))
    if existing_user:
        return None, "existing"

    execute(
        "insert into users (name, email, password_hash) values (?, ?, ?)",
        (
            name,
            email,
            ph,
        ),
    )

    user_id = fetch_one("select id from users where email = ?;", (email,))

    payload = {
        "user_id": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }

    token = jwt.encode(payload, key, algorithm="HS256")

    return token, None


def login_user(email, password):
    user = fetch_one("select * from users where email = ?", (email,))
    try:
        PasswordHasher().verify(user["password_hash"], password)
    except:
        return None, "password incorrect"

    payload = {
        "user_id": str(user["id"]),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }

    token = jwt.encode(payload, key, algorithm="HS256")

    return token, None
