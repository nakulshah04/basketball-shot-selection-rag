import os

import pytest

from backend.rag.retriever import get_retriever


pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="Requires local embeddings and the Chroma vector store.",
)
def test_retrieval_smoke():
    retriever = get_retriever()
    docs = retriever.invoke("late shot clock three pointer under tight defense")

    assert docs


if __name__ == "__main__":
    retriever = get_retriever()
    docs = retriever.invoke("late shot clock three pointer under tight defense")

    for d in docs[:3]:
        print(d.page_content)
