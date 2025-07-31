from ai_model import embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from get_yt_vid import get_script
import faiss
from pipelines import organize_docs
import numpy as np

url = "https://youtu.be/swCPic00c30?si=ilTIOvLTkI8AUl20"

script = get_script(url)

documents = [
    "This is the first document, talking about Langchain.",
    "Another document that discusses FAISS and semantic search.",
    "Here’s a third document on using LLMs for organization."
]
def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=50000,
            chunk_overlap=2000,
            length_function=len
        )

    return text_splitter.split_text(text)


# Convert documents to embeddings
if len(script) > 50_000:
    documents = split_text(script)
print(len(documents))

# embedding_vectors = embeddings.embed_documents(documents)
# embedding_vectors = np.array(embedding_vectors).astype(np.float32)

# # FAISS: Create the index (dim = embedding size)
# dim = embedding_vectors.shape[1]  # Size of embedding vector
# index = faiss.IndexFlatL2(dim)  # Using L2 distance metric

# # Add embeddings to FAISS index
# index.add(embedding_vectors)
# # Query to search for
# query = "Tell me about Langchain and how it works with FAISS."

# # Convert the query to an embedding
# query_embedding = embeddings.embed_query(query)

# # Perform the search in FAISS
# k = 3  # Top k most similar documents to retrieve
# query_embedding = np.array(query_embedding).astype(np.float32).reshape(1, -1)
# distances, indices = index.search(query_embedding, k)

# # Retrieve and print the most similar documents
# for i in indices[0]:
#     print(documents[i])  # Print the document based on similarity




