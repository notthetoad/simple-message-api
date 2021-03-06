from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database import Base
from .main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
  try:
    db = TestingSessionLocal()
    yield db
  finally:
    db.close()

app.dependency_overrides[get_db] = override_get_db

API_KEY = '?api_key=helloworld'

client = TestClient(app)

def test_create_message():
  response = client.post(
    f'/message{API_KEY}',
    json={"text": "hello world"}
  )
  assert response.status_code == 201, response.text
  data = response.json()
  assert data['text'] == 'hello world'
  assert 'id' in data
  msg_id = data['id']

  response = client.get(f"/message/{msg_id}")
  assert response.status_code == 200, response.text
  data = response.json()
  assert data['text'] == 'hello world'
  assert data['id'] == msg_id

def test_update_message():
  response = client.post(
    f'/message{API_KEY}',
    json={"text": "hello world"}
  )
  assert response.status_code == 201, response.text
  data = response.json()
  assert data['text'] == 'hello world'
  assert 'id' in data
  msg_id = data['id']

  response = client.patch(
    f'/message/{msg_id}{API_KEY}',
    json={"text": "foobar"}
  )
  assert response.status_code == 200, response.text
  data = response.json()
  assert data['text'] == 'foobar'
  assert data['id'] == msg_id

def test_delete_message():
  response = client.post(
    f'/message{API_KEY}',
    json={"text": "hello world"}
  )
  assert response.status_code == 201, response.text
  data = response.json()
  assert data['text'] == 'hello world'
  assert 'id' in data
  msg_id = data['id']

  response = client.delete(
    f'/message/{msg_id}{API_KEY}'
  )
  assert response.status_code == 200
  assert response.json() == {"deleted_message_id": msg_id}

def test_create_message_unauthorized():
  response = client.post(
    '/message',
    json={"text": "hello world"}
  )
  assert response.status_code == 403
  assert response.json() == {"detail": "Forbidden"}

def test_update_message_unauthorized():
  response = client.post(
    f'message{API_KEY}',
    json={"text": "hello world"}
  )
  assert response.status_code == 201, response.text
  data = response.json()
  assert data['text'] == 'hello world'
  assert 'id' in data
  msg_id = data['id']

  response = client.patch(
    f'/message/{msg_id}',
    json={"text": "foobar"}
  )
  assert response.status_code == 403
  assert response.json() == {"detail": "Forbidden"}

def test_delete_message_unauthorized():
  response = client.post(
    f'message{API_KEY}',
    json={"text": "hello world"}
  )
  assert response.status_code == 201, response.text
  data = response.json()
  assert data['text'] == 'hello world'
  assert 'id' in data
  msg_id = data['id']

  response = client.delete(
    f'/message/{msg_id}'
  )
  assert response.status_code == 403
  assert response.json() == {"detail": "Forbidden"}