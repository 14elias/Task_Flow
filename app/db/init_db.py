from app.db.session import Base, engine
from app.models.user import User
from app.models.project import Project, ProjectTeam
from app.models.team import Team, TeamMember
from app.models.notification import Notification
from app.models.comment import Comment
from app.models.task import Task, TaskStatus

def init_db():
    print("Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")
