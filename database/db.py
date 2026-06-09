from dotenv import load_dotenv
import sqlite3
from datetime import datetime

db_path = "instance/todo.db"

load_dotenv()


def get_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
            create table if not exists users (
                id integer primary key autoincrement,
                name text not null, 
                email text unique not null, 
                password_hash text not null, 
            )
            """)
    conn.commit()
    conn.execute("""
            create table if not exists tasks (
                id integer primary key autoincrement, 
                user_id integer not null, 
                title text not null,
                description text not null, 
                FOREIGN KEY (user_id) REFERENCES users(id)
                ON DELETE CASCADE
            )
                """)
    conn.commit()
    conn.close()


def execute(query, params=()):
    conn = get_db()
    conn.execute(query, params)
    conn.commit()
    conn.close()


def fetch_one(query, params=()):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return row


def fetch_many(query, params=()):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchmany()
    conn.close()
    return rows
