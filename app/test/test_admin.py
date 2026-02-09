from .utils import *
from app.routers.admin import get_db, get_current_user
from fastapi import status

from app.main import app
from app.routers.todos import Todos


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    print(response.json()) == [{'priority': 3, 'id': 1, 'owner_id': 1, 'title': 'Play with pandas', 'description': 'python book', 'complete': False}]
    
def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None    
    
def test_admin_delete_not_found_todo(test_todo):
    response = client.delete("/admin/todo/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'todo not found'}
