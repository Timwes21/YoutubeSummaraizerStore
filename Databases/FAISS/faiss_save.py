from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from pathlib import Path
import shutil
from ai_model import embeddings
import os


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
    if os.path.exists(path):
        return
    library.save_local(path)

def get_local(path):
    return FAISS.load_local(path, embeddings=embeddings, allow_dangerous_deserialization=True)

def delete_store(path):
    folder = Path(f"timwes21/{path}")
    shutil.rmtree(folder)

def save_to_hive(library, username):
    filepath = f"{username}/hive"
    if os.path.exists(filepath):
        existing = FAISS.load_local(filepath, embeddings, allow_dangerous_deserialization=True)
        existing.merge_from(library)
        existing.save_local(filepath)
        return
    save_to_store(library, filepath)

def create_knowledge_base(username, base_name):
    path = f"{username}/knowledge_bases/{base_name}"
    if os.path.exists(path):
        return
    os.makedirs(path)


# def save_local(self, folder_path: str, index_name: str = "index") -> None:
#         """Save FAISS index, docstore, and index_to_docstore_id to disk.

#         Args:
#             folder_path: folder path to save index, docstore,
#                 and index_to_docstore_id to.
#             index_name: for saving with a specific index file name
#         """
#         path = Path(folder_path)
#         path.mkdir(exist_ok=True, parents=True)

#         # save index separately since it is not picklable
#         faiss = dependable_faiss_import()
#         faiss.write_index(self.index, str(path / f"{index_name}.faiss"))

#         # save docstore and index_to_docstore_id
#         with open(path / f"{index_name}.pkl", "wb") as f:
#             pickle.dump((self.docstore, self.index_to_docstore_id), f)

#     @classmethod
#     def load_local(
#         cls,
#         folder_path: str,
#         embeddings: Embeddings,
#         index_name: str = "index",
#         *,
#         allow_dangerous_deserialization: bool = False,
#         **kwargs: Any,
#     ) -> FAISS:
#         """Load FAISS index, docstore, and index_to_docstore_id from disk.

#         Args:
#             folder_path: folder path to load index, docstore,
#                 and index_to_docstore_id from.
#             embeddings: Embeddings to use when generating queries
#             index_name: for saving with a specific index file name
#             allow_dangerous_deserialization: whether to allow deserialization
#                 of the data which involves loading a pickle file.
#                 Pickle files can be modified by malicious actors to deliver a
#                 malicious payload that results in execution of
#                 arbitrary code on your machine.
#         """
#         if not allow_dangerous_deserialization:
#             raise ValueError(
#                 "The de-serialization relies loading a pickle file. "
#                 "Pickle files can be modified to deliver a malicious payload that "
#                 "results in execution of arbitrary code on your machine."
#                 "You will need to set `allow_dangerous_deserialization` to `True` to "
#                 "enable deserialization. If you do this, make sure that you "
#                 "trust the source of the data. For example, if you are loading a "
#                 "file that you created, and know that no one else has modified the "
#                 "file, then this is safe to do. Do not set this to `True` if you are "
#                 "loading a file from an untrusted source (e.g., some random site on "
#                 "the internet.)."
#             )
#         path = Path(folder_path)
#         # load index separately since it is not picklable
#         faiss = dependable_faiss_import()
#         index = faiss.read_index(str(path / f"{index_name}.faiss"))

#         # load docstore and index_to_docstore_id
#         with open(path / f"{index_name}.pkl", "rb") as f:
#             (
#                 docstore,
#                 index_to_docstore_id,
#             ) = pickle.load(  # ignore[pickle]: explicit-opt-in
#                 f
#             )

#         return cls(embeddings, index, docstore, index_to_docstore_id, **kwargs)

