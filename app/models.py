from sqlalchemy import (
  Column,
  Integer,
  Text
)
from .database import Base

class Message(Base):
  __tablename__ = "message"

  id = Column(Integer, primary_key=True)
  text = Column(Text, nullable=False)
  counter = Column(Integer, default=0)