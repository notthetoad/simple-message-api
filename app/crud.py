from . import schemas
from database import create_connection
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey

API_KEY = "helloworld"
API_KEY_NAME = "api_key"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
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

async def create_message(db: create_connection, text: schemas.MessageRequest, api_key: ApiKey = Depends(get_api_key)):
  curr = db.cursor()
  curr.execute("SELECT INTO message (text) VALUES (?)", (text.text, ))
  db.commit()
  return