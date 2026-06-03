from flask import Flask, request
from services.db import *
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


@app.route("/register", methods=["POST"])
def register():
    user = request.get_json()
    try:
        result = register_user(user)
        if result:
            return 201
    except Exception as e:
        return {"error": f"unable to register - {e}"}, 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port, host="0.0.0.0")
