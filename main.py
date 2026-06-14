from langchain_core.messages import HumanMessage
from my_agent import app  # Importing the compiled graph from agent.py

if __name__ == "__main__":
    query = "Who is the current Prime Minister of Greece?"
    inputs = {"messages": [HumanMessage(content=query)]}
    
    print("Starting Modular Agent")
    
    try:
        # Using invoke to get the complete final state directly
        config = {"configurable": {"thread_id": "1"}}
        result = app.invoke(inputs, config=config)
        
        print("\n================== FINAL ANSWER ==================")
        # Retrieving the very last message in the state sequence
        final_message = result["messages"][-1]
        print(f"AI: {final_message.content}")
        print("==================================================")
        
    except Exception as e:
        print(f"An error occurred during execution: {e}")