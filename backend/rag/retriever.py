from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from backend.config import get_settings

settings = get_settings()

def get_retriever(k=5):
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model
    )
    vectordb = Chroma(
        persist_directory=str(settings.chroma_persist_dir),
        embedding_function=embeddings
    )
    return vectordb.as_retriever(search_kwargs={"k": k})
