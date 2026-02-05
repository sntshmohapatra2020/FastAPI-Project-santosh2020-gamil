from fastapi.testclient import TestClient
from app.main import app
from fastapi import status


client = TestClient(app)



