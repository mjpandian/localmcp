# Local MCP SQLite3 Agent with Ollama

## Project Summary

This project implements a local AI-powered agent that interacts with a SQLite database using the Model Context Protocol (MCP). It enables natural language queries to add, search, and retrieve data from a local database, leveraging Ollama for LLM inference and LlamaIndex for agent orchestration. The design emphasizes reliability for local development by using Stdio transport, avoiding network dependencies.

## Architecture

![Architecture Diagram](architecture.gif)

### Key Technologies
- **MCP (Model Context Protocol)**: Standardizes tool calling between AI models and external resources.
- **Ollama**: Runs open-source LLMs locally (e.g., Llama 3.2 3B) for privacy and offline capability.
- **SQLite3**: Lightweight, file-based database for simple data storage and retrieval.
- **LlamaIndex**: Framework for building LLM applications with tool integration.
- **Python**: Core language for server and client implementation.

### Design Highlights
- **Stdio Transport**: Uses standard input/output for MCP communication, ensuring stability in local setups without HTTP overhead.
- **Modular Architecture**: Separates server (tool definitions) and client (agent logic) for easy extension.
- **Tool-Based Interaction**: Defines database operations as MCP tools, allowing the AI to call them dynamically.
- **Auto-Generated Database**: Database file is created on first use, with no manual setup required.

This README covers the setup for a local MCP (Model Context Protocol) environment using Ollama and SQLite3. This setup uses the Stdio transport method, which is the most reliable for local development.

## Project Structure

- `server.py`: The MCP Server containing the SQLite tools.
- `ollama-client.py`: The AI Agent that connects to Ollama and orchestrates tool calls.
- `mcp_database.sqlite3`: The local database file (auto-generated).

## Prerequisites

- Python 3.10+
- Ollama: [Download here](https://ollama.ai/)
- Required Model:

  ```bash
  ollama pull llama3.2:3b
  ```
  (Note: Using a 3B model is recommended for machines with ~8-10GB RAM.)

## Installation

1. Clone or create your project directory:

   ```bash
   mkdir local-mcp && cd local-mcp
   ```

2. Install dependencies:

   We recommend using `uv` for fast management, but standard pip works too:

   ```bash
   pip install mcp llama-index-llms-ollama llama-index-tools-mcp httpx
   ```

## How to Run

1. The Server (`server.py`)

   Ensure your `server.py` uses the standard MCP run command and has no print() statements outside of the tools (as they interfere with Stdio).

2. The Client (`ollama-client.py`)

   Ensure your client is configured to point to the server file:

   ```python
   mcp_tool = McpToolSpec(
       command="python",
       args=["server.py"]
   )
   ```

3. Execution

   Since we are using Stdio transport, you do not need to run the server separately. The client will launch the server as a background process automatically.

   Run the client:

   ```bash
   python ollama-client.py
   ```

## Usage Examples

Once the prompt `>` appears, you can interact with your database in natural language:

| Action        | Example Command                     |
|---------------|-------------------------------------|
| Add Data      | `> add a new record called "Project Alpha"` |
| Search        | `> do we have anything about "Project"?` |
| Fetch All     | `> get all records`                |
| Exit          | `> quit`                            |