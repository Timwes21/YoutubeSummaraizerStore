from fastapi import APIRouter, Depends
import pydantic_models
from Databases.redis.redis_client import change_knowlegde_source
from Databases.postgres import dependencies
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from Databases.postgres import db_models, dependencies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Databases.redis.redis_client import change_chat
from fastapi.responses import JSONResponse
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

start_path = os.environ["MNT_PATH"]

router = APIRouter()
        
@router.post("/messages")
async def get_messages(context: pydantic_models.Context, db: AsyncSession = Depends(dependencies.get_db)):
    try:
        result = await db.execute(
            select(db_models.Message)
            .where(db_models.Message.user_id == context.username)
            .where(db_models.Message.context == context.context)
        )
        messages = result.scalars().all()
    except DBAPIError as e:
        print(e)
        await db.rollback()
        result = await db.execute(
            select(db_models.Message)
            .where(db_models.Message.user_id == context.username)
            .where(db_models.Message.context == context.context)
        )
        messages = result.scalars().all()
    change_chat(context.username, messages[0:20])
    return messages


@router.post("/get-knowledge-lists", response_class=JSONResponse)
async def get_knowlegde_lists(user_info: pydantic_models.UserInfo):
    username = user_info.username
    loop = asyncio.get_event_loop()
    try:
        videos = await asyncio.gather(loop.run_in_executor(None, lambda: os.listdir(f"{start_path}/{username}/videos")))
        videos = videos[0]
    except Exception as e:
        print(e)
        videos = []
    return {"videos": videos}


@router.post("/get-knowledge-source", response_class=JSONResponse)
async def get_knowlegde_source(knowlegde_source: pydantic_models.KnowledgeSource):
    print(knowlegde_source)
    if knowlegde_source.type == "hive":
        path = knowlegde_source.name
    else:
        path = f"{knowlegde_source.type}/{knowlegde_source.name}"
        
    change_knowlegde_source(knowlegde_source.username, path)
