import os
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode


#Agent (with buily-in tools)
#We are going to use the Duck Duck go search tool
query = "Who is the current Prime Minister of Greece?"
tools = [DuckDuckGoSearchRun()]

model= ChatOllama(model="llama3.2", temperature=0.3)
model_with_tools = model.bind_tools(tools)
print("\nAI: ", model.invoke(query))

search= DuckDuckGoSearchRun() #Search tool
print("\nSearch:", search.invoke(query))

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def model_call(state:AgentState) ->AgentState:
 system_prompt= SystemMessage(content=
                              "You are my AI assistant, please answer my query to the best of your ability"
 )
 response=model_with_tools.invoke([system_prompt] +state["messages"])
 return {"messages": [response]}

#Underlying action behind the conditional edge
def should_continue(state: AgentState):
    messages= state ["messages"]
    last_message= messages [-1]

    #This code checks if there are any gurther tiol calling requires in the last message
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"
    
#Creation of our graph again
graph= StateGraph(AgentState)
graph.add_node("our_agent", model_call)
tool_node= ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point('our_agent')

#How to create conditional edge
graph.add_conditional_edges(
    "our_agent", #origin
    should_continue, #underlying action
    {#Different edges along with their destinations
        "continue": "tools",
        "end": END,
        },
)

graph.add_edge("tools", "our_agent")

app=graph.compile()

#Function to make the output more aesthetic
def print_stream(stream):
    for s in stream:
        message=s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


inputs= {"messages": [("user", query)]}
print_stream(app.stream(inputs, stream_mode= "values"))




