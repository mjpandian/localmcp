from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.tools.mcp import McpToolSpec, BasicMCPClient
from llama_index.core.agent.workflow import FunctionAgent, ToolCallResult, ToolCall
 
from llama_index.core.workflow import Context
from httpx import Timeout

 
# LlamaIndex handles the underlying httpx timeout using this parameter
llm = Ollama(
    model="qwen3:0.6b", 
    request_timeout=300.0
)
Settings.llm = llm

SYSTEM_PROMPT = """You are an AI assistant for a SQLite database.
- To see everything in the database, call 'fetch_data' with the query 'all'.
- To add data, use 'add_data'.
- If a user asks for 'all records', remember to pass the string 'all' to the tool."""

async def get_agent(tools: McpToolSpec):
    tools = await tools.to_tool_list_async()
    agent = FunctionAgent(
        name="Agent with Ollama LLM",
        description="An agent that uses Ollama LLM to interact with tools.",
        tools=tools,
        llm=llm,
        system_prompt=SYSTEM_PROMPT,
    )
    return agent

async def handle_user_message(
    agent: FunctionAgent,
    message_context: str,
    agent_context: Context,
    verbose: bool = False,
):
    handler = agent.run(user_msg=message_context, ctx=agent_context)
    
    async for event in handler.stream_events():
        if verbose:
            if isinstance(event, ToolCall):
                # FIX: Change tool_args to tool_kwargs
                # Some versions might also use event.tool_selection.tool_kwargs
                args = getattr(event, 'tool_kwargs', 'No arguments found')
                print(f"DEBUG: Tool Call -> {event.tool_name} with args {args}")
                
            elif isinstance(event, ToolCallResult):
                print(f"DEBUG: Tool Result -> {event.tool_output}")
    
    response = await handler
    return str(response)

async def main():
    mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
    mcp_tool = McpToolSpec(mcp_client)
    agent = await get_agent(mcp_tool)

    context = Context(agent)
    while True:
        msg = input("> ")
        if msg.lower() in ["exit", "quit"]:
            break
        resp = await handle_user_message(agent, msg, context, verbose=True)
        print(f"Agent Response: {resp}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

