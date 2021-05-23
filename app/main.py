import sqlite3

from fastapi import FastAPI, Depends, Security, HTTPException
from database import create_connection
from . import schemas
from . import crud
from fastapi.security.api_key import APIKey


app = FastAPI()

# @app.post('/message', status_code=201)
# async def create_message(db: create_connection):
  # msg_text = text.text
  # curr = app.db_connection.cursor()
  # curr.execute("INSERT INTO message (text) VALUES (?)", (msg_text, ))
  # app.db_connection.commit()
  # return

@app.post('/message', status_code=201)
async def create_message(text: schemas.MessageRequest, db: create_connection = Depends(create_connection, api_key: APIKey = Depends(crud.get_api_key))):
  msg = crud.create_message(db, text, api_key)

@app.patch('/message/{message_id}')
async def update_message(text: MessageRequest, message_id: int, api_key: APIKey = Depends(get_api_key)):
  msg_text = text.text
  curr = app.db_connection.cursor()
  curr.execute("UPDATE message SET text = ?, counter = 0 WHERE id = ?", (msg_text, message_id, ))
  app.db_connection.commit()
  return

@app.delete('/message/{message_id}')
async def delete_message(message_id: int, api_key: APIKey = Depends(get_api_key)):
  curr = app.db_connection.cursor()
  curr.execute("DELETE FROM message WHERE id = (?)", (message_id, ))
  app.db_connection.commit()
  return

# Returning list instead of JSON
@app.get('/message/{message_id}', status_code=200)
# async def get_message(message_id: int):
def get_message(message_id: int):
  app.db_connection.row_factory = sqlite3.Row
  curr = app.db_connection.cursor()
  curr.execute("UPDATE message SET counter = counter + 1 WHERE id = (?)", (message_id, ))
  app.db_connection.commit()
  msg = curr.execute("SELECT text, counter from message WHERE id = (?)", (message_id, )).fetchone()
  return {"text": msg['text'], "counter": msg['counter']}

@app.get('/test', status_code=200)
async def get_test():
  return