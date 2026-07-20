# 📚 Task Manager / Todo List API

A simple RESTful Todo List API built with Flask and SQLite.

This project allows users to create an account, log in securely, and manage personal tasks through a clean and structured API.

🔗 Roadmap Project Reference:  
https://roadmap.sh/projects/todo-list-api

---

# 📖 What this project is

This is a backend web API that acts like the server behind a todo list/task manager application.

Instead of a graphical interface, this project works through HTTP requests (like sending messages to a server).

It allows users to:

- Create an account
- Log in securely
- Receive an authentication token (JWT)
- Create personal tasks
- View only their own tasks
- Update or delete tasks
- Navigate tasks using pagination

Each user has their own private space of tasks, meaning no user can see or access another user’s data.

---

# 🔐 Authentication (JWT Explained Simply)

This project uses JWT (JSON Web Tokens) to manage login sessions.

### What this means:

When you log in:

- The server generates a token (a long encoded string)
- That token represents your identity
- You send that token with every request after login

### Why this is used:

- No need to store sessions on the server
- Each request is independently verified
- More secure and scalable than traditional sessions

### Example token usage:

Authorization: Bearer <your_token_here>

---

# 🧠 How the system works (simple flow)

1. User registers or logs in
2. Server returns a JWT token
3. User stores this token (Postman or request headers)
4. Every protected request uses this token
5. Server decodes token → extracts user_id
6. Only that user’s tasks are accessed

---

# ✨ Features

## 👤 User System

- Register new users
- Login authentication
- Password hashing (Argon2)
- Email validation

## 📝 Task System

- Create tasks
- View tasks (paginated)
- Update tasks (partial updates supported)
- Delete tasks
- Each user sees only their own tasks

## 🔐 Security

- JWT authentication
- Protected routes using decorators
- Secure password hashing
- Foreign key constraints in SQLite

## 📄 Pagination

- Tasks are split into pages
- Default: 10 tasks per page
- Page controlled via query parameter

---

# 🧠 First Run Behaviour (Important)

On first startup:

- The SQLite database `todo.db` is automatically created
- The `.env` file is automatically generated
- A secret key is automatically created for JWT signing

👉 You do NOT need to manually create any database or config file.

---

# 🛠 Technology Stack

| Technology | Purpose               |
| ---------- | --------------------- |
| Python     | Programming language  |
| Flask      | Web framework         |
| SQLite     | Database              |
| PyJWT      | Token authentication  |
| Argon2     | Password hashing      |
| dotenv     | Environment variables |

---

# 📂 Project Structure

```text
Todo List API/
│
├── app.py
│
├── database/
│     └── db.py
│
├── services/
│     ├── auth.py
│     ├── config.py
│     ├── task_services.py
│     └── user_services.py
│
├── instance/
│     └── todo.db
│
└── requirements.txt
```

---

# ⚙️ Setup Instructions

## 1. Clone the repository

### Terminal

`git clone https://github.com/sheikh-h/Task-Manager-Api.git`<br>
`cd Task-Manager-Api`

---

## 2. Create virtual environment

### macOS / Linux

`python3 -m venv venv`<br>
`source venv/bin/activate`

### Windows

`python -m venv venv`<br>
`venv\Scripts\activate`

---

## 3. Install dependencies

`pip install -r requirements.txt`

---

## 4. Run the application

`flask run`

or

`python app.py`

The API will start at:

`http://127.0.0.1:5000`

or

`localhost:5000/`

---

# 🔐 Using Authentication (IMPORTANT)

After registering or logging in, you will receive a JWT token.

You must include this token in all protected requests.

---

## 🟣 Postman (Recommended)

### How to add token:

1. Open Postman
2. Go to the request you want to test
3. Click **Authorization tab**
4. Select **Type: Bearer Token**
5. Paste your JWT token

Postman will automatically attach it to all requests.

---

## 🔵 cURL (manual method)

You must manually add the token to headers for every request after login or registration:

```bash
-H "Authorization: Bearer <your_token_here>"
```

---

# 📬 API Endpoints

---

## 👤 Register User

### POST /register

### Postman:

- Method: POST
- URL:
  `http://127.0.0.1:5000/register`
- Body → raw → JSON:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

### cURL:

```bash
curl -X POST "http://127.0.0.1:5000/register" \
-H "Content-Type: application/json" \
-d '{
"name": "John Doe",
"email": "john@example.com",
"password": "securepassword"
}'
```

---

## 🔑 Login User

### POST /login

### Postman:

- Method: POST
- URL:
  `http://127.0.0.1:5000/login`
- Body → raw → JSON:

```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

### cURL:

```bash
curl -X POST "http://127.0.0.1:5000/login" \
-H "Content-Type: application/json" \
-d '{
"email": "john@example.com",
"password": "securepassword"
}'
```

---

## 📝 Get All Tasks (Paginated)

### GET /tasks?page=1

### Postman:

- Method: GET
- URL:
  `http://127.0.0.1:5000/tasks?page=1`
- Go to Authorization tab
- Select Bearer Token
- Paste JWT token

### cURL:

```bash
curl -X GET "http://127.0.0.1:5000/tasks?page=1" \
-H "Authorization: Bearer <your_token_here>"
```

---

## ➕ Create Task

### POST /add-tasks

### Postman:

- Method: POST
- URL:
  `http://127.0.0.1:5000/add-tasks`
- Body → raw → JSON:

```json
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "status": "pending"
}
```

- Add Bearer token in Authorization tab

### cURL:

```bash
curl -X POST "http://127.0.0.1:5000/add-tasks" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_token_here>" \
-d '{
"title": "Buy groceries",
"description": "Milk, bread, eggs",
"status": "pending"
}'
```

---

## ✏️ Update Task

### PUT /task/<id>

### Postman:

- Method: PUT
- URL:
  `http://127.0.0.1:5000/task/1`
- Body → raw → JSON:

```json
{
  "title": "Updated task"
}
```

- Add Bearer token in Authorization tab

### cURL:

```bash
curl -X PUT "http://127.0.0.1:5000/task/1" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_token_here>" \
-d '{
"title": "Updated task"
}'
```

---

## ❌ Delete Task

### DELETE /task/<id>

### Postman:

- Method: DELETE
- URL:
  `http://127.0.0.1:5000/task/1`
- Add Bearer token in Authorization tab

### cURL:

```bash
curl -X DELETE "http://127.0.0.1:5000/task/1" \
-H "Authorization: Bearer <your_token_here>"
```

---

# 📄 Pagination

Tasks are returned in pages:

- Default limit: 10 tasks per page
- Page controlled using:

`/tasks?page=1`

Response includes:

- page number
- total tasks
- total pages

---

# 🧠 Design Principles

- REST API structure
- Stateless authentication (JWT)
- Modular service-based architecture
- User data isolation
- Clean separation of concerns

---

# 🚀 Future Improvements

- Task filtering (status, search)
- Sorting options
- Refresh token system
- Rate limiting
- Frontend interface (React or HTML UI)
- Docker support

---

# 🤝 Final Notes

This project was built as part of backend learning practice.

It demonstrates:

- How authentication works in real systems
- How APIs manage user-specific data
- How pagination improves data handling
- How JWT replaces traditional session systems

Some concepts were learned and refined using documentation, experimentation, and AI-assisted learning to better understand backend design patterns.
There are some future improvements that I would like to make to this project like sorting and filtering tasks, rate limiting, refresh token mechanism and more.

# 📄 Licence

This project is licensed under the MIT Licence - see the `LICENSE` file for full details.

```text
MIT Licence

Copyright (c) 2026 Sheikh Hussain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

# 🤝 Connect With Me

<div align="center">

<a href="https://github.com/Sheikh-H">
<img src="https://img.shields.io/badge/GitHub-376e00?style=flat&logo=github&logoColor=white" alt="GitHub">
</a>

<a href="https://www.linkedin.com/in/sheikh-hussain/">
<img src="https://img.shields.io/badge/LinkedIn-376e00?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn">
</a>

<a href="mailto:sheikh.hussain1155@gmail.com">
<img src="https://img.shields.io/badge/Gmail-376e00?style=flat&logo=gmail&logoColor=white" alt="Gmail">
</a>

<a href="https://sheikh-hussain.onrender.com/">
<img src="https://img.shields.io/badge/Portfolio-376e00?style=flat&logo=github&logoColor=white" alt="Portfolio">
</a>

</div>

---

<p align="center">
Built with Python, Flask, and SQLite by <strong>Sheikh Hussain</strong> 💚
</p>

<p align="center">
⭐ If you found this project useful, consider giving it a star on GitHub.
</p>
