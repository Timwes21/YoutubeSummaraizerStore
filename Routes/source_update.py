from fastapi import APIRouter
from get_yt_vid import get_script, get_video_info
from fastapi.responses import JSONResponse
from pipelines import organize_docs
import pydantic_models
from Databases.FAISS import faiss_save 
from Databases.redis.redis_client import change_knowlegde_source
import os
import httpx
import asyncio
import shutil

router = APIRouter()


async def create_library(url):
    script = get_script(url)
    title, author = await get_video_info(url)
    # organized_docs = organize_docs(script)
    library = faiss_save.create_library(script)
    return title, author, library

@router.post("/save-url", response_class=JSONResponse)
async def read_url(video: pydantic_models.Video):
    try:
        title, author, library = create_library(video.url)
        print("got library")
        faiss_save.save_to_store(library, f"{video.username}/videos/{author}:{title}")
        print("saved video")
        await faiss_save.save_to_hive(library, video.username)
        print("saved to store")
        return {"added": "yes"}
    except Exception as e:
        print(e)
        return {"added": "no"}
    

@router.post("/get-video-rq", response_class=JSONResponse)
async def get_video_rq(video: pydantic_models.Video):
    print(video)
    title, author, library = await create_library(video.url)
    print("got video")
    path = f"short-term/{author}:{title}"
    faiss_save.save_to_store(library=library, path=f"{video.username}/{path}")
    print("saved to store")
    change_knowlegde_source(id=video.username, path=path)
    return {"saved": "yes", "title": title, "author": author}
    # except Exception as e:
        # print("error: ", e)
        # return {"saved": "no"}



    
@router.post("/forget-user")
async def forget_user(uuid: pydantic_models.Uuid):
    if uuid.token in os.listdir():
        shutil.rmtree(uuid.token)




    

