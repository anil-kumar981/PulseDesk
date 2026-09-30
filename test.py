from fastapi.testclient import TestClient
from app import app
client = TestClient(app)
response = client.post("/api/auth/auth/register", json={
  "first_name": "Anil",
  "last_name": "yadav",
  "email": "yadavanilkumar8113@gmail.com",
  "password": "@Anil123"
})
print(response.json())
