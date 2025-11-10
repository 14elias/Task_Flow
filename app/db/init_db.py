from app.db.session import Base, engine

def init_db():
    print("Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")
