from pydantic import BaseModel, PositiveInt, constr

# REQUESTS
class MessageRequest(BaseModel):
  text: constr(min_length=1, max_length=160)

# RESPONSES
class MessageResponse(BaseModel):
  text: constr(min_length=1, max_length=160)
  counter: PositiveInt

# USER MODEL
class User(BaseModel):
  username: str
  