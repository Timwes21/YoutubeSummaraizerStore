from sqlalchemy import Column, String, Text, DateTime, Integer, UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Message(Base):
    __tablename__ = "m3"
    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    user_id = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    role = Column(String, nullable=False)
    context = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow())


# from sqlmodel import Field, Session, SQLModel, create_engine, select


# class Hero(SQLModel, table=True):
#     id: str = Field(default=lambda: str(uuid.uuid4()), primary_key=True)
#     user_id: str = Field(index=True)
#     message: str = Field(index=True)
#     role: str = Field(index=True)
#     context: str = Field(index=True)
#     timestamp: DateTime = Field(index=True, default=datetime.utcnow)
