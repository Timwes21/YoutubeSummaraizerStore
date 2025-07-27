from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from Databases.postgres import db_models, dependencies
from Routes.get_info import router as info_router
from Routes.source_update import router as source_router
from Routes.talk_to_source import router as ws_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with dependencies.engine.begin() as conn:
        await conn.run_sync(db_models.Base.metadata.create_all)
    yield
    





app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           
    allow_credentials=True,
    allow_methods=["*"],           
    allow_headers=["*"],           
)

app.include_router(ws_router, prefix="/talk-to-source")
app.include_router(source_router, prefix="/update-sources")
app.include_router(info_router, prefix="/get-info")





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port="8000")