from dotenv import load_dotenv
from pathlib import Path
import sqlite3

db_path  = "instance/todo.db"

load_dotenv()


def get_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    Path("instance").mkdir(exist_ok=True)
    conn = get_db()
    
    conn.execute("""
            create table if not exists users (
                id integer primary key autoincrement,
                name text not null, 
                email text unique not null, 
                password_hash text not null, 
                created_at timestamp default current_timestamp
            )
            """)
    conn.commit()
    conn.close()
    

def register_user(user):
    
    new_user = {
        'name' = user['name'], 
        'email' = user['email'], 
        'password_hash' = password_hash,
    }
