from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from IPython.display import Image, display

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
    base_url="https://api.siliconflow.cn/v1",
    api_key=SecretStr("sk-omeyhkplymcxsmecpafribmmjminnapohmliahddzdxrxtfv"),
    temperature=0.0,
    streaming=True,
)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    # 返回一个State dict
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

# 绘制 graph 图
try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("AI:", value["messages"][-1].content)

while True:
    try:
        user_input = input("YOU: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        print("YOU: " + user_input)
        stream_graph_updates(user_input)
        break


