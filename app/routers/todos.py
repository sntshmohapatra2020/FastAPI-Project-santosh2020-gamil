from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field

from ..database import SessionLocal
from ..models import Todos
from .auth import get_current_user

router = APIRouter(
    tags= ['todo'],
    prefix='/todo'
)

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
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail='Authentication Falied')
    return db.query(Todos).filter(Todos.id == user.get('id')).all()



@router.post("/createtodo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,
                      db: db_dependency,
                      todo_request: TodoRequest):
    if not user:
        raise HTTPException(status_code=401, detail='authentication failed')
    todo_model = Todos(**todo_request.model_dump(), \
        owner_id = user.get('id'))

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return todo_model


@router.get("/getbyid/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo(user: user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).\
        filter(Todos.owner_id == user.get('id')).first()

    if todo_model:
        return todo_model

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID {todo_id} does not exist"
    )
    
@router.put("/modifytodo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def modify_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id : int= Path(gt=0)):
    if not user:
        raise HTTPException(status_code=401, detail='authentication failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).\
        filter(Todos.owner_id == user.get('id')).first()
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'todo with id {todo_id} is not found')
    todo_model.title = todo_request.title  
    todo_model.description = todo_request.description 
    todo_model.priority = todo_request.priority 
    todo_model.complete = todo_request.complete
    db.commit()
    return 

@router.delete("/deletetodo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=401, detail='authentication failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).\
        filter(Todos.owner_id == user.get('id')).first()
    if not todo_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} is not found"
        )
    db.delete(todo_model)
    db.commit()
    return
    