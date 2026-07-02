from backend.utils.prompts import DECISION_PROMPT, CRITIC_PROMPT
from backend.agents.nodes import decision_node, critic_node
from backend.rag.retriever import get_retriever
from backend.config import get_settings
from langgraph.graph import StateGraph, END

settings = get_settings()


def prepare_retry_node(state):
    critique = state.get("critique") or {}
    state["retries"] = state.get("retries", 0) + 1
    state["query"] += "\n\nCritic feedback: " + critique.get("reason", "")
    return state

def build_graph():
    graph = StateGraph(dict)

    graph.add_node("decision", decision_node)
    graph.add_node("critic", critic_node)
    graph.add_node("prepare_retry", prepare_retry_node)

    graph.set_entry_point("decision")

    def route(state):
        critique = state.get("critique") or {}
        retries = state.get("retries", 0)
        if critique.get("valid") is False and retries < settings.max_agent_retries:
            return "prepare_retry"
        return END

    graph.add_conditional_edges(
        "critic",
        route,
        {
            "prepare_retry": "prepare_retry",
            END: END
        }
    )

    graph.add_edge("decision", "critic")
    graph.add_edge("prepare_retry", "decision")

    return graph.compile()

def run_agent(query):
    retriever = get_retriever(k=settings.retriever_k)
    docs = retriever.invoke(query)
    context = "\n".join([d.page_content for d in docs])

    graph = build_graph()

    state = {
        "query": query,
        "context": context,
        "retries": 0,
        "decision_prompt": DECISION_PROMPT,
        "critic_prompt": CRITIC_PROMPT
    }

    return graph.invoke(state)
