from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END

# Εισαγωγή από τα δικά μας modules
from config import tools
from model import model_with_tools

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(
        content=(
            "You are my AI Secretary Assistant. Your main responsibility is to retrieve the official documents, "
            "email layouts, and application templates that the user needs.\n\n"
            "RULES:\n"
            "1. Do NOT make up your own templates from your internal knowledge.\n"
            "2. You MUST USE the 'fetch_office_template' tool to retrieve the exact template that the user asks for.\n"
            "3. Fill in any brackets like [Your Name] if the user provides that information in their query.\n"
            "4. For general knowledge or current events, use the internet search tool."
        )
    )
    response = model_with_tools.invoke([system_prompt] + state["messages"])
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


graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

graph.add_edge("tools", "our_agent")

app = graph.compile()



