import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
load_dotenv()

api_key = os.environ['GOOGLE_API_KEY']
llm = ChatGoogleGenerativeAI(api_key=api_key, verbose=True, model="gemini-2.0-flash")
embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001', api_key=api_key)