from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
import os

from backend.config import get_settings
from backend.utils.json_utils import normalize_critique, normalize_decision

settings = get_settings()

llm = ChatOllama(
    model=settings.llm_model,
    temperature=settings.llm_temperature,
)

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def decision_node(state):
    messages = [
        SystemMessage(content="You are a decision-making agent."),
        HumanMessage(
            content=state["decision_prompt"].format(
                context=state["context"],
                query=state["query"]
            )
        )
    ]
    response = llm.invoke(messages)
    state["decision"] = normalize_decision(response.content)
    return state

def critic_node(state):
    messages = [
        SystemMessage(content="You are a strict validation agent."),
        HumanMessage(
            content=state["critic_prompt"].format(
                decision=state["decision"],
                context=state["context"]
            )
        )
    ]
    response = llm.invoke(messages)
    state["critique"] = normalize_critique(response.content)
    return state
