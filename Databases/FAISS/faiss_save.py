from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from pathlib import Path
import shutil
from ai_model import embeddings
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()
start_path = os.environ["MNT_PATH"]

def create_library(docs):
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
                chunk_overlap=100,
            length_function=len
        )

    docs = text_splitter.split_documents(docs)

    library = FAISS.from_documents(docs, embeddings)
    return library

def save_to_store(library, path):
    path = f"{start_path}/{path}"
    if os.path.exists(path):
        return
    library.save_local(path)

def get_local(path):
    path = f"{start_path}/{path}"
    return FAISS.load_local(path, embeddings=embeddings, allow_dangerous_deserialization=True)

def delete_store(path, username):
    path = f"{start_path}/{username}/{path}"
    folder = Path(path)
    shutil.rmtree(folder)



async def save_to_hive(library, username):
    filepath = f"{username}/hive"
    def do_task():
        if os.path.exists(filepath):
            existing = FAISS.load_local(filepath, embeddings, allow_dangerous_deserialization=True)
            existing.merge_from(library)
            existing.save_local(filepath)
            return
        save_to_store(library, filepath)
    await asyncio.to_thread(do_task)

def create_knowledge_base(username, base_name):
    path = f"{username}/knowledge_bases/{base_name}"
    if os.path.exists(path):
        return
    os.makedirs(path)

