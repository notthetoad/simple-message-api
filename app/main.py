from fastapi import FastAPI, Depends, Security, HTTPException
from fastapi.security.api_key import APIKey
from sqlalchemy.orm import Session
from . import schemas, crud
from .database import get_db
from .crud import get_api_key


app = FastAPI()


@app.post('/message', status_code=201)
async def create_message(text: schemas.MessageRequest, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
  result = crud.create_message(db, text, api_key)
  return {"text": result.text, "id": result.id}

@app.patch('/message/{message_id}', status_code=200, response_model=schemas.MessageResponse)
async def update_message(message_id: int, text: schemas.MessageRequest, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
  result = crud.update_message(db, message_id, text, api_key)
  if result == False:
    raise HTTPException(status_code=404)
  return result

@app.delete('/message/{message_id}', status_code=200)
async def delete_message(message_id: int, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
  result = crud.delete_message(db, message_id, api_key)
  if result == False:
    raise HTTPException(status_code=404)
  return {"deleted_message_id": message_id}

@app.get('/message/{message_id}', status_code=200, response_model=schemas.MessageResponse)
async def get_message(message_id: int, db: Session = Depends(get_db)):
  message = crud.get_message(db, message_id)
  if message == False:
    raise HTTPException(status_code=404)
  return message