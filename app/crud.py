from sqlalchemy.orm import Session
from fastapi import Security, Depends, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from .schemas import MessageRequest
from .models import Message

API_KEY = "helloworld"
API_KEY_NAME = "api_key"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


def get_api_key(
  api_key_query: str = Security(api_key_query),
  api_key_header: str = Security(api_key_header),
  api_key_cookie: str = Security(api_key_cookie)
):
  if api_key_query == API_KEY:
    return api_key_query
  elif api_key_header == API_KEY:
    return api_key_header
  elif api_key_cookie == API_KEY:
    return api_key_cookie
  else:
    raise HTTPException(status_code=403)

def create_message(db: Session, text: MessageRequest, api_key: APIKey):
  db_msg = Message(text=text.text)
  db.add(db_msg)
  db.commit()
  return db_msg

def update_message(db: Session, message_id: int, text: MessageRequest, api_key: APIKey):
  db_msg: Message = db.query(Message).filter(Message.id == message_id).first()
  if db_msg is None:
    return False
  db_msg.text = text.text
  db_msg.counter = 0
  db.commit()
  return db_msg

def delete_message(db: Session, message_id: int, api_key: APIKey):
  db_msg: Message = db.query(Message).filter(Message.id == message_id).first()
  if db_msg is None:
    return False
  db.delete(db_msg)
  db.commit()
  return True

def get_message(db: Session, message_id: int, api_key: APIKey):
  db_msg: Message = db.query(Message).filter(Message.id == message_id).first()
  db_msg.counter += 1
  db.commit()
  if db_msg is None:
    return False
  return db_msg