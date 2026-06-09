import os
import secrets


def ensure_env_file():
    if not os.path.exists(".env"):
        key = secrets.token_hex(16)
        with open(".env", "w") as f:
            f.write(f"SECRET_KEY={key}\n")
