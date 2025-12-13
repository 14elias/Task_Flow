from fastapi import FastAPI
from app.api.v1 import (
    user_routes, 
    auth_routes, 
    team_routes, 
    project_routes,
    task_ruotes,
    comment_routes
)
from .db.init_db import init_db
from app.core.websocket_manager import manager
from app.api.websocket import notification_socket 
# from .db.session import Base, engine

app = FastAPI()
app.include_router(user_routes.router, tags=["user"])
app.include_router(auth_routes.router, tags=["auth"])
app.include_router(team_routes.router, tags=["team"])
app.include_router(project_routes.router, tags=["project"])
app.include_router(task_ruotes.router, tags=["task"])
app.include_router(comment_routes.router, tags=["comment"])
app.include_router(notification_socket.router, tags=["socket"])


# @app.on_event("startup")
# async def start():
#     print("Creating all database tables...")
#     await init_db()


@app.on_event("startup")
async def on_startup():
    await manager.startup()

@app.on_event("shutdown")
async def on_shutdown():
    await manager.shutdown()


@app.get('/')
async def main():
    return ("Hello from taskflow!")


from app.celery_tasks.tasks import send_email_task
@app.post("/test-email")
async def test_email():
    send_email_task.delay(123, {"type": "welcome", "payload": {"email": "eliasmebrahtom1994@gmail.com"}})
    return {"status": "queued"}

@app.post("/test-b-email")
async def test_b_email():
    send_email_task(123, {"type": "welcome", "payload": {"email": "eliasmebrahtom1994@gmail.com"}})
    return {"status": "queued"}


if __name__ == "__main__":
    main()
