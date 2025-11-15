import uuid
import pytest

from app.models.user import User
from app.core.security import get_password_hash, create_refresh_token


@pytest.fixture
def test_create_user(db_session):
    user = User(
        username=f"user_{uuid.uuid4().hex}",
        email=f"user_{uuid.uuid4().hex}@example.com",
        hashed_password=get_password_hash("password123"),
        is_active=True,
        role='user'
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_signup(client):
    response = client.post("/signup", json = {"username":f"elias_{uuid.uuid4().hex}","email":f"ella_{uuid.uuid4().hex}@gmail.com","password":"ella"})

    assert response.status_code == 200

def test_incorrect_signup(client):
    response = client.post("/signup", json = {"username":f"elias_{uuid.uuid4().hex}","email":f"ella_{uuid.uuid4().hex}@gmail.com"})

    assert response.status_code == 422

def test_login(client, test_create_user):
    response = client.post('/login', data={'username':test_create_user.username, 'password':"password123"})

    assert response.status_code == 200

def test_refresh_token(client,test_create_user):
    refresh_token = create_refresh_token(data={'sub':test_create_user.username})
    response = client.post('/refresh', params={"refresh_token": refresh_token})

    assert response.status_code == 200