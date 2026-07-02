from backend.agents.decision_graph import run_agent
import os

import pytest


pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="Requires Ollama and the local vector store.",
)
def test_agent_smoke():
    query = "8 seconds left, down by 2, defender 1 meter away on left wing"

    result = run_agent(query)

    assert result["decision"]
    assert result["critique"]


if __name__ == "__main__":
    query = "8 seconds left, down by 2, defender 1 meter away on left wing"
    result = run_agent(query)

    print("\nDECISION:")
    print(result["decision"])

    print("\nCRITIQUE:")
    print(result["critique"])
