from datetime import datetime
from database.db import *
from argon2 import PasswordHasher


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
    return "registered"
