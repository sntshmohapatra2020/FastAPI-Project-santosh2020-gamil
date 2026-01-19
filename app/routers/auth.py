from fastapi import APIRouter, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

from ..database import SessionLocal
from ..models import User

router = APIRouter()

bcrypt_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
    )


class CreateUserRequest(BaseModel):
    email : str
    username : str
    first_name : str
    last_name : str
    password : str
    is_active : bool


def get_db():
    """
    Dependency that provides a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Type alias for cleaner dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username : str, password : str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_user(db: db_dependency):
    """
    Retrieve all users from the database table User.
    """
    return db.query(User).all()


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
        )

    db.add(create_user_model)
    db.commit()
    

@router.post("/token")
async def login_for_access_token(form_data: 
    Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "authentication Falied"
    return "successful authentication"
