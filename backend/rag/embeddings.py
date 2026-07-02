from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from backend.config import get_settings

settings = get_settings()

def build_vectorstore():
    with open(settings.shot_corpus_txt) as f:
        texts = [line.strip() for line in f.readlines() if line.strip()]

    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model
    )

    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory=str(settings.chroma_persist_dir)
    )
    
    print(f"Stored {len(texts)} embeddings")

if __name__ == "__main__":
    build_vectorstore()
