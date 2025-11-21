import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base
from app import main
from app.db.session import get_db
import app.models





TEST_DB_URL = "sqlite:///./test.db"
# TEST_DB_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

connection = engine.connect()

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=connection,  # bind to the single Connection
)

@pytest.fixture(scope="session", autouse=True)
def set_up_test_db():
    # ensure clean schema every test session
    Base.metadata.drop_all(bind=connection)
    Base.metadata.create_all(bind=connection)
    yield
    Base.metadata.drop_all(bind=connection)
    connection.close()
    engine.dispose()

@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

@pytest.fixture(autouse=True)
def override_get_db(db_session):
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass
    main.app.dependency_overrides[get_db] = _get_test_db
    yield
    main.app.dependency_overrides.clear()


@pytest.fixture
def client():
    """FastAPI TestClient that uses the overridden DB."""
    with TestClient(main.app) as c:
        yield c


