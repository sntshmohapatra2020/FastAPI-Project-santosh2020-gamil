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
async def get_all(db: db_dependency):
    """
    Retrieve all todo items from the database table.
    """
    return db.query(Todos).all()


@router.post("/createtodo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,
                      db: db_dependency,
                      todo_request: TodoRequest):
    """
    Create a new Todo item.
    """
    if not user:
        raise HTTPException(status_code=401, detail='authentication failed')
    todo_model = Todos(**todo_request.model_dump(), owner_id = user['id'])

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return todo_model


@router.get("/getbyid/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    """
    Retrieve a single Todo item by its ID.

    Args:
        db (Session): Database session dependency.
        todo_id (int): ID of the Todo item to retrieve.
                        Must be greater than 0.

    Returns:
        Todos: The Todo object if found.

    Raises:
        HTTPException: 
            - 404 if the Todo item does not exist.
    """

    # Query the database for the todo with the given ID
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    # If the todo exists, return it
    if todo_model:
        return todo_model

    # If no todo is found, raise a 404 error
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID {todo_id} does not exist"
    )
    
@router.put("/modifytodo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def modify_todo(db: db_dependency, todo_request: TodoRequest, todo_id : int= Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'todo with id {todo_id} is not found')
    todo_model.title = todo_request.title  
    todo_model.description = todo_request.description 
    todo_model.priority = todo_request.priority 
    todo_model.complete = todo_request.complete
    db.commit()
    return 

@router.delete("/deletetodo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    """
    Delete a Todo item by its ID.

    Args:
        db (Session): Database session injected via dependency.
        todo_id (int): ID of the Todo item to delete.
                       Must be greater than 0.

    Raises:
        HTTPException:
            - 404: If the Todo item does not exist.
    """

    # Fetch the todo item from the database
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    # If the todo does not exist, raise a 404 error
    if not todo_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} is not found"
        )

    # Delete the todo item
    db.delete(todo_model)

    # Commit the transaction to persist deletion
    db.commit()

    # 204 No Content → return nothing
    return
    