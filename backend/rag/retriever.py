from langchain_chroma import Chroma
from backend.config import get_settings
from backend.rag.embeddings import get_embeddings

settings = get_settings()

def get_retriever(k=5):
    vectordb = Chroma(
        collection_name=settings.chroma_collection,
        persist_directory=str(settings.chroma_persist_dir),
        embedding_function=get_embeddings()
    )
    return vectordb.as_retriever(search_kwargs={"k": k})
