from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from fastapi import FastAPI,Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import nest_asyncio

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
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

# FastAPI 部分
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/chat")
async def chat_endpoint(message: str = Query(..., description="用户输入")):
    user_input = message
    print("YOU: " + user_input)

    # 只取 content 字段
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            response = value["messages"][-1].content
            print("AI: " + response)
            return response

# 如果需要直接运行
# 访问示例 GET http://localhost:8000/chat?message=你好
nest_asyncio.apply()
uvicorn.run(app, host="0.0.0.0", port=8000)
