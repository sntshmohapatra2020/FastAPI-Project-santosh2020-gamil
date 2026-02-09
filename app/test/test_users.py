from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status
from app.main import app

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_users(test_users):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['email'] == "santosh@gmail.com"
    assert response.json()['username'] == "santosh"
    assert response.json()['id'] == 1
    assert response.json()['role'] == "admin"
    assert response.json()['first_name'] == "santosh"
    assert response.json()['last_name'] == "mohapatra"
    assert response.json()['is_active'] == True

def test_change_password_success(test_users):
    response = client.put("/users/password", 
                          json={
                              "password": "testpassword",
                                "new_password": "newpassword"
                                }
                          )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    