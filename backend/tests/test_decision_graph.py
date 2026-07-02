from backend.agents import decision_graph


def test_graph_retries_invalid_critique_then_finishes(monkeypatch):
    attempts = {"count": 0}

    def fake_decision_node(state):
        attempts["count"] += 1
        state["decision"] = {
            "shot": "3PT",
            "explanation": "Context supports an open perimeter shot.",
            "confidence": 0.7,
        }
        return state

    def fake_critic_node(state):
        state["critique"] = {
            "valid": attempts["count"] > 1,
            "reason": "Needs tighter grounding.",
        }
        return state

    monkeypatch.setattr(decision_graph, "decision_node", fake_decision_node)
    monkeypatch.setattr(decision_graph, "critic_node", fake_critic_node)
    monkeypatch.setattr(decision_graph.settings, "max_agent_retries", 2)

    graph = decision_graph.build_graph()
    result = graph.invoke({
        "query": "late clock, open at top of key",
        "context": "A prior top of key 3PT was made with space.",
        "retries": 0,
        "decision_prompt": "{context}\n{query}",
        "critic_prompt": "{decision}\n{context}",
    })

    assert attempts["count"] == 2
    assert result["critique"]["valid"] is True
    assert result["retries"] == 1
