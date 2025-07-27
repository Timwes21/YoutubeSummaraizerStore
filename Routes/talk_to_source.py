from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
import json
from pipelines import get_response
from Databases.redis.redis_client import get_knowlegde_source_name
from Databases.postgres import db_models, schemas, dependencies
from Databases.FAISS import faiss_save 

users_qas = {}

router = APIRouter()

@router.websocket("/talk-to-video/{id}")
async def talk_to_video(ws: WebSocket, id : str, db: AsyncSession = Depends(dependencies.get_db)):
    path = get_knowlegde_source_name(id)
    if path == None:
        await ws.close(reason="No knowledge Source Selected")
        return
    await ws.accept()
    library = faiss_save.get_local(path)
    retriever = library.as_retriever()
    users_qas[id] = retriever
    try: 
        while True:
            print("***********************************************")
            print("this is usersqa: ", users_qas)
            data = await ws.receive_text()
            print("***********************************************")
            print("here is the data: ", data)
            parsed = json.loads(data)
            results = await users_qas[id].ainvoke(parsed["message"])
            print("***********************************************")
            print("here is the results: ", results)
            reply = get_response(results, parsed["message"], id, parsed["context"])
            print("***********************************************")
            print("here is the reply", reply)
            await ws.send_text(reply)
            if parsed["context"] != "newUrl":
                user_message_format = schemas.MessageCreate(user_id=id, message=parsed["message"], role="user", context=parsed["context"])
                user_message = db_models.Message(**user_message_format.model_dump())
                db.add(user_message)

                ai_message_format = schemas.MessageCreate(user_id=id, message=reply, role="ai", context=parsed["context"])
                ai_message = db_models.Message(**ai_message_format.model_dump())
                db.add(ai_message)
                await db.commit()
    except WebSocketDisconnect as e:
        print(e)


