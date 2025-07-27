from pydantic import BaseModel, Field
from typing import Literal

class UserInfo(BaseModel):
    username: str

class OrganizedDoc(BaseModel):
    metadata: str = Field(description="A unique identifier for the body of text to make it easy to find appropriate info")
    content: str

class Docs(BaseModel):
    docs: list[OrganizedDoc]
    video_summary: str = Field(description="A summary of the video that makes it easy to identitfy the kind of info it gives when looking for knwoledge sources")

class NewMessage(BaseModel):
    html_message: str

class Video(UserInfo):
    url: str

class Base(BaseModel):
    name: str

class Context(UserInfo):
    context: str

class KnowledgeSource(UserInfo):
    type: str = Literal["hive", "videos", "knowledge_bases"]
    name: str

class Uuid(BaseModel):
    token: str

