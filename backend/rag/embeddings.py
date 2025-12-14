from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

CORPUS_PATH = "backend/rag/shot_corpus.txt"
PERSIST_DIR = "backend/rag/chroma_db"

def build_vectorstore():
    with open(CORPUS_PATH) as f:
        texts = [line.strip() for line in f.readlines() if line.strip()]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )
    
    print(f"Stored {len(texts)} embeddings")

if __name__ == "__main__":
    build_vectorstore()