from pydantic import BaseModel, PositiveInt, constr

# REQUESTS
class MessageRequest(BaseModel):
  text: constr(min_length=1, max_length=160)

  class Config:
    orm_mode = True

# RESPONSES
class MessageResponse(BaseModel):
  id: int
  text: constr(min_length=1, max_length=160)
  counter: int

  class Config:
    orm_mode = True

  