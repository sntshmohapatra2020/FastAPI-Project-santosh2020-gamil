from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi import status
import pytest

from app.database import Base

from app.main import app
from app.models import Todos, User
from app.routers.todos import get_db, get_current_user
from .test_main import TestClient
from app.routers.auth import bcrypt_context


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass = StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'santosh', 'id':1, 'role': 'admin'}


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Play with pandas",
        id = 1,
        description = "python book",
        priority = 3,
        complete = False,
        owner_id = 1
    )
    
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield db
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_users():
    user = User(
            email = "santosh@gmail.com",
            username = "santosh",
            id = 1,
            hashed_password = bcrypt_context.hash("testpassword"),
            role = "admin",
            first_name = "santosh",
            last_name = "mohapatra",
            is_active = True
        )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    db.close()
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()