from datetime import datetime, timedelta
from database.db import *
from argon2 import PasswordHasher
import jwt
from flask import request


def register_user(name, email, password):
    now = datetime.now().replace(microsecond=0)

    ph = PasswordHasher().hash(password)

    # First see if there is a user with the same email and return error
    existing_user = fetch_one("select * from users where email = ?", (email,))
    if existing_user:
        return "existing"

    execute(
        "insert into users (name, email, password_hash, created_at) values (?, ?, ?, ?)",
        (
            name,
            email,
            ph,
            now,
        ),
    )
    return None, "registered"


def login_user(email, password):
    user = fetch_one("select * from users where email = ?", (email,))

    try:
        PasswordHasher().verify(user["password_hash"], password)
    except:
        return None, "password incorrect"

    payload = {
        "user_id": user["id"],
        "expires": datetime.utcnow() + timedelta(minutes=30),
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token, None
