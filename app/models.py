from sqlalchemy import (
  Column,
  Integer,
  Text
)
from .database import Base, engine

class Message(Base):
  __tablename__ = "message"

  id = Column(Integer, primary_key=True)
  text = Column(Text, nullable=False)
  counter = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)