from backend.utils.prompts import DECISION_PROMPT, CRITIC_PROMPT
from backend.agents.nodes import decision_node, critic_node
from backend.rag.retriever import get_retriever
from langgraph.graph import StateGraph, END

def build_graph():
    graph = StateGraph(dict)

    graph.add_node("decision", decision_node)
    graph.add_node("critic", critic_node)

    graph.set_entry_point("decision")

    def route(state):
        critique = state.get("critique", {})
        if isinstance(critique, dict) and critique.get("valid") is False:
            state["query"] += "\n\nCritic feedback: " + critique.get("reason", "")
            return "decision"
        return END

    graph.add_conditional_edges(
        "critic",
        route,
        {
            "decision": "decision",
            END: END
        }
    )

    graph.add_edge("decision", "critic")

    return graph.compile()

def run_agent(query):
    retriever = get_retriever()
    docs = retriever.invoke(query)
    context = "\n".join([d.page_content for d in docs])

    graph = build_graph()

    state = {
        "query": query,
        "context": context,
        "decision_prompt": DECISION_PROMPT,
        "critic_prompt": CRITIC_PROMPT
    }

    return graph.invoke(state)