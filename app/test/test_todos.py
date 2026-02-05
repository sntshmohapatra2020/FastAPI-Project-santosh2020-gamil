from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi import status
import pytest

from app.database import Base
from app.main import app
from app.models import Todos
from app.routers.todos import get_db, get_current_user
from .test_main import TestClient
from .utils import override_get_current_user, \
    override_get_db, TestingSessionLocal, engine, client, test_todo


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get("/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{ 'title' : "Play with pandas",
        'id':1,
        'description' : "python book",
        'priority' : 3,
        'complete' : False,
        'owner_id' : 1}]
    
def test_read_one_authenticated(test_todo):
    response = client.get("/todo/getbyid/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id']== 1

def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todo/getbyid/1111")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':"Todo with ID does not exist"}
    
def test_create_todo(test_todo):
    request_data = {
        'title': 'play with python',
        'description': 'python book',
        'priority': 3,
        'complete': True
        }
    response = client.post("/todo/createtodo/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
    
def test_update_todo(test_todo):
    request_data = {
        'title': 'master mysql',
        'description': 'RDBM book',
        'priority': 2,
        'complete': False
    }

    response = client.put("/todo/modifytodo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data["title"]


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'master mysql',
        'description': 'RDBM book',
        'priority': 2,
        'complete': False
    }

    response = client.put("/todo/modifytodo/100", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'todo with id is not found'}
    
def test_delete_todo(test_todo):
    response = client.delete("/todo/deletetodo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
    
    
def test_delete_todo(test_todo):
    response = client.delete("/todo/deletetodo/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail":"Todo with ID is not found"}