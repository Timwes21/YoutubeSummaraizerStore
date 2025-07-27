from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    user_id: str
    message: str
    role: str
    context: str

class MessageOut(BaseModel):
    id: str
    user_id: str
    message: str
    role: str
    timestamp: datetime
