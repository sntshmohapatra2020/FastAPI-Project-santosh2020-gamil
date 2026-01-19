from fastapi import FastAPI
from .routers import auth, todos
from .models import Base
from .database import engine, Base

app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)

Base.metadata.create_all(bind=engine)