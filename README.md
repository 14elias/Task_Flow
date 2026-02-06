```markdown
# 🚀 Taskflow API

Taskflow is a **high-performance, asynchronous project management and notification system** built with **FastAPI**. It enables modern team collaboration through real-time updates, role-based access control (RBAC), and scalable background processing.

---

## ✨ Features

### 🔐 Authentication & Security

- JWT-based authentication with **Access and Refresh tokens**
- **OAuth2 scopes** for fine-grained permissions (`admin`, `manager`, `member`)
- Secure password hashing using **Argon2/Bcrypt**

### 👥 Team & Project Management

- Organize users into teams
- Assign teams to projects
- Track deadlines and responsibilities

### ✅ Tasks & Comments

- Task lifecycle: **Pending → In-Progress → Done**
- Threaded commenting system for collaboration

### 🔔 Real-time Notifications

Hybrid notification system using:

- **Redis Pub/Sub + WebSockets** for live updates
- **Celery + Redis** for background email delivery

### 🔄 Fully Asynchronous Core

- Built with **SQLAlchemy 2.0 + AsyncSession**
- Designed for performance and scalability

### 🧪 Testing

- High test coverage using **pytest**
- Isolated testing environment with SQLite

---

## 🛠️ Tech Stack

| Component      | Technology                          |
| -------------- | ----------------------------------- |
| Framework      | FastAPI (Python 3.10+)              |
| Database       | PostgreSQL + SQLAlchemy 2.0 (Async) |
| Task Queue     | Celery + Redis                      |
| Real-time      | WebSockets + Redis Pub/Sub          |
| Authentication | python-jose, pwdlib                 |
| Validation     | Pydantic v2                         |

---

## 📁 Project Structure
```

app/
├── api/ # Route handlers (v1, WebSockets)
├── core/ # Config, Security, WebSocket Manager
├── crud/ # Async DB logic
├── models/ # SQLAlchemy ORM Models
├── schemas/ # Pydantic models
├── services/ # Business logic (Notifications)
├── celery_tasks/ # Background workers
└── db/ # Database sessions & migrations

````

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

Make sure you have installed:
- **Python 3.10+**
- **PostgreSQL**
- **Redis**

---

### 2️⃣ Environment Setup

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/taskflow
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256

REDIS_URL=redis://localhost:6379/0
REDIS_PUB_URL=redis://localhost:6379/4

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=noreply@taskflow.com
````

---

### 3️⃣ Installation

```bash
git clone https://github.com/youruser/taskflow.git
cd taskflow
pip install -r requirements.txt
```

---

## ⚙️ Running the System

### ▶️ Start the API

```bash
uvicorn app.main:app --reload
```

Then open:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### ▶️ Start Celery Worker

```bash
celery -A app.core.celery_app worker --loglevel=info
```

---

### ▶️ WebSocket Endpoint

```
ws://localhost:8000/ws/notifications
```

> Requires a valid JWT token as a query parameter.

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🛡️ Role-Based Access Control (RBAC)

| Role       | Scopes              | Permissions                            |
| ---------- | ------------------- | -------------------------------------- |
| **Admin**  | `me, admin, delete` | Full system access                     |
| **Member** | `me`                | Profile access, task updates, comments |

---

## 📬 Notification Flow

When an important event occurs (e.g., a task assignment):

1. **Persist** → Notification is saved in the database
2. **WebSocket Push** → Sent via Redis Pub/Sub
3. **History Stored** → Added to Redis recent list
4. **Email Queued** → Sent in background via Celery

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📄 License

MIT License — feel free to use and modify.
