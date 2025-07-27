import os
from dotenv import load_dotenv
import redis
import json
from typing import Literal
load_dotenv()



r = redis.from_url(url=os.environ["REDIS_URL"], socket_connect_timeout=5,socket_timeout=5,retry_on_timeout=True,)


def get_chat_name(username):
    return f"{username}:chat"


def add_to_chat(username, message: str, writer: str = Literal["AI", "user"]):
    print("this should be username", username)
    log = {writer: message}
    r.rpush(get_chat_name(username), json.dumps(log))



def get_recent_chat(username) -> list[dict]:
    logs = r.lrange(get_chat_name(username), 0, -1)
    logs: list = [i.decode() for i in logs]
    if len(logs) > 20:
        r.lpop(get_chat_name(username))
    print(logs)
    return logs

def change_chat(username, messages: list):
    r.delete(get_chat_name(username))
    logs = [r.rpush(get_chat_name(username), json.dumps({i.role: i.message})) for i in messages]
    print("logs: ", logs)

def change_knowlegde_source(id, path):
    r.set(id, f"{id}/{path}")

def get_knowlegde_source_name(id: str):
    a = r.get(id)
    if a == None:
        return a
    return a.decode()