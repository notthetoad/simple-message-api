import sqlite3

from fastapi import FastAPI, Request
from models import MessageRequest, MessageResponse

app = FastAPI()

# TODO auth, secret sharing ? idk
# TODO only auth requests can add, update, delete

@app.on_event('startup')
async def startup():
  app.db_connection = sqlite3.connect('main.db')

@app.on_event('shutdown')
async def shutdown():
  app.db_connection = sqlite3.close()

@app.post('/message', status_code=201)
async def create_message(text: MessageRequest):
  msg_text = text.text
  curr = app.db_connection.cursor()
  curr.execute("INSERT INTO message (text) VALUES (?)", (msg_text, ))
  app.db_connection.commit()
  return

@app.patch('/message/{message_id}')
async def update_message(text: MessageRequest, message_id: int):
  # Update message
  msg_text = text.text
  curr = app.db_connection.cursor()
  curr.execute("UPDATE message SET text = ?, counter = 0 WHERE id = ?", (msg_text, message_id, ))
  app.db_connection.commit()
  return

@app.delete('/message/{message_id}')
async def delete_message(message_id: int):
  curr = app.db_connection.cursor()
  curr.execute("DELETE FROM message WHERE id = (?)", (message_id, ))
  app.db_connection.commit()
  return

# Returning list instead of JSON
@app.get('/message/{message_id}', status_code=200)
async def get_message(message_id: int):
  curr = app.db_connection.cursor()
  curr.execute("UPDATE message SET counter = counter + 1 WHERE id = (?)", (message_id, ))
  app.db_connection.commit()
  msg = curr.execute("SELECT text, counter from message WHERE id = (?)", (message_id, )).fetchone()
  return msg
