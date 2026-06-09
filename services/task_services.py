import jwt
from flask import request
import os
from dotenv import load_dotenv

load_dotenv()

key = os.environ.get("SECRET_KEY")


def all_tasks():
    jwt.decode()
