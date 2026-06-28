# AI Assistant Secretary Agent (using LangGraph)

This repository contains the implementation of a local, autonomous AI Secretary Assistant Agent. The system is built using the LangGraph framework and Llama 3.2 (3B) hosted locally via Ollama. 

The agent utilizes the ReAct (Reasoning + Acting) architecture to process natural language requests in Greek, dynamically determine when external data retrieval is necessary, and extract structured document templates (emails, applications, and corporate forms) from local text files (.txt, .md) or structured datasets (.json).


## System Architecture

-Parsing and State Routing: The model evaluates the user's query to identify targeted variables (e.g., names, companies, time or date) and specific document requests.
-Orchestration:Built on LangGraph's StateGraph architecture to manage conversational state, multi-step routing, and tool execution loops.
-Template Retrieval: Custom python tool implementation (`fetch_office_template`) capable of parsing localized plain text files, markdown files, and structured JSON data sources.
-Output Alignment: Advanced prompt engineering configurations applied to enforce professional vocabulary, context preservation, and translation error correction during placeholder extraction.

## System Requirements & Installation

1. Python Environment Setup
-Python 3.10 version is installed. Install the core dependencies via pip:

```bash
pip install langgraph langchain-core langchain-ollama

2. Local Model Deployment
```bash
ollama pull llama3.2


## Repository Structure
-config.py (Hybrid multi-format dataset parsers and tools)
-model.py (Local model)
-my_agent.py (State definition, system node and LangGraph workflow)
-main.py (Execution)
-email_data.json (Structured Alpaca-style instruction template dataset)
-templates/ (Storage directory containing local .md and .txt reference files)


## Usage Guide
Ensure that the Ollama framework is active and running in your system's background, then execute the runtime script from the root directory:

```bash
python main.py
