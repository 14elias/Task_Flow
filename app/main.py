from fastapi import FastAPI
from app.api.v1 import user_routes, auth_routes
from .db.init_db import init_db
from .db.session import Base, engine

app = FastAPI()
app.include_router(user_routes.router, tags=["user"])
app.include_router(auth_routes.router, tags=["auth"])


@app.on_event("startup")
def start():
    # Base.metadata.drop_all(bind=engine)
    init_db()

@app.get('/')
def main():
    return ("Hello from taskflow!")


if __name__ == "__main__":
    main()
