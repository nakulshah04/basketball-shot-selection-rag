import json

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from backend.config import get_settings

settings = get_settings()

def get_embeddings():
    return OllamaEmbeddings(model=settings.embedding_model)


def build_vectorstore():
    with settings.shot_corpus_jsonl.open(encoding="utf-8") as file:
        documents = [Document(**json.loads(line)) for line in file if line.strip()]
    if not documents:
        raise RuntimeError("Corpus is empty. Build it before embedding.")
    Chroma.from_documents(
        documents=documents,
        embedding=get_embeddings(),
        persist_directory=str(settings.chroma_persist_dir)
        ,collection_name=settings.chroma_collection
    )
    return len(documents)

if __name__ == "__main__":
    print(f"Stored {build_vectorstore():,} local Ollama embeddings")
