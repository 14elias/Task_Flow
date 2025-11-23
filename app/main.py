from fastapi import FastAPI
from app.api.v1 import user_routes, auth_routes, team_routes, project_routes, task_ruotes
from .db.init_db import init_db
# from .db.session import Base, engine

app = FastAPI()
app.include_router(user_routes.router, tags=["user"])
app.include_router(auth_routes.router, tags=["auth"])
app.include_router(team_routes.router, tags=["team"])
app.include_router(project_routes.router, tags=["project"])
app.include_router(task_ruotes.router, tags=["task"])

@app.on_event("startup")
def start():
    # Base.metadata.drop_all(bind=engine)
    init_db()

@app.get('/')
def main():
    return ("Hello from taskflow!")


if __name__ == "__main__":
    main()
