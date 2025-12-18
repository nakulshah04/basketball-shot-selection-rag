from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
load_dotenv()
import os

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
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
    state["decision"] = response.content
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
    state["critique"] = response.content
    return state