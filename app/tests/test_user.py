import pytest
import uuid
import json

from app.core.security import get_password_hash, create_access_token
from app.models.user import User

@pytest.fixture
def test_create_admin(db_session):
    user = User(
        username=f"admin_{uuid.uuid4().hex}",
        email=f"admin_{uuid.uuid4().hex}@example.com",
        hashed_password=get_password_hash("password123"),
        is_active=True,
        role='admin'
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

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


@pytest.fixture
def admin_token(test_create_admin):
    return create_access_token(data={"sub":test_create_admin.username, "scope":"me admin"})

@pytest.fixture
def user_token(test_create_user):
    return create_access_token(data={"sub":test_create_user.username, "scope":"me"})



def test_admin_me(client, admin_token, test_create_admin):
    response = client.get('/user/me', headers={"Authorization": f"Bearer {admin_token}"})

    assert response.status_code == 200
    assert response.json().get('username') == test_create_admin.username

def test_user_me(client, user_token,test_create_user):
    response = client.get('/user/me', headers={"Authorization": f"Bearer {user_token}"})

    assert response.status_code == 200
    assert response.json().get('username') == test_create_user.username

def test_unautorized_me(client):
    response = client.get('/user/me', headers={"Authorization": f"Bearer"})

    assert response.status_code == 401

def test_delete_user_by_admin(client, admin_token, test_create_user):
    response = client.delete(
        '/user/delete',headers={"Authorization": f"Bearer {admin_token}"},
        params={"username": test_create_user.username}
    )

    assert response.status_code == 200

def test_delete_user_by_user(client, user_token, test_create_admin):
    response = client.delete(
        '/user/delete',
        headers={"Authorization": f"Bearer {user_token}"},
        params={"username": test_create_admin.username}
    )

    assert response.status_code == 403

def test_get_all_user_by_admin(client, admin_token):
    response = client.get('/user/all',headers={"Authorization": f"Bearer {admin_token}"})

    assert response.status_code == 200

def test_get_all_user_by_user(client, user_token):
    response = client.get('/user/all',headers={"Authorization": f"Bearer {user_token}"})

    assert response.status_code == 403

def test_deactivate_user_by_admin(client, admin_token, test_create_user):
    response = client.patch(
        '/user/deactivate', 
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"username": test_create_user.username}
    )

    assert response.status_code == 200

def test_deactivate_user_by_user(client, user_token, test_create_admin):
    response = client.patch(
        '/user/deactivate', 
        headers={"Authorization": f"Bearer {user_token}"},
        params={"username": test_create_admin.username}
    )

    assert response.status_code == 403


def test_update_user(client, user_token):
    response = client.patch(
        '/user/update',
        headers={"Authorization": f"Bearer {user_token}"},
        json={'username':f'ellaman_{uuid.uuid4().hex}', "email":f"ella_{uuid.uuid4().hex}@gmail.com"}
    )

    assert response.status_code == 200

def test_incorrect_update_user(client, user_token):
    response = client.patch(
        '/user/update',
        headers={"Authorization": f"Bearer {user_token}"},
        json={'username':f'ellaman_{uuid.uuid4().hex}', "email":f"ella_{uuid.uuid4().hex}@gmail.com", "role":"admin"}
    )

    assert response.status_code == 422