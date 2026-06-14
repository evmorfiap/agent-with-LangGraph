from langchain_ollama import ChatOllama
from config import tools

# Init local LLM
model = ChatOllama(model="llama3.2", temperature=0.3)

model_with_tools = model.bind_tools(tools)