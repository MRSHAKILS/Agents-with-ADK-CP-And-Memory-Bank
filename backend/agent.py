import os
import sys
from pathlib import Path
from google.adk import Agent
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool.mcp_toolset import StdioConnectionParams
from mcp.client.stdio import StdioServerParameters
from dotenv import load_dotenv

# Explicitly load .env from the backend directory (same dir as this script)
_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

# System instruction for the agent
SYSTEM_INSTRUCTION = (
    "You are a GitHub profile analyst and dev card generator. When a user gives you a GitHub username, "
    "you ALWAYS follow this exact sequence: first call scrape_github, then analyze_profile with the result, "
    "then generate_card_html with all three inputs, then save_card. Never skip steps. "
    "Be enthusiastic about developers' work. If the profile is private or doesn't exist, say so clearly."
)

# Define the toolset connecting to the local MCP server via stdio
# Note: We use sys.executable to ensure we use the same python interpreter/venv
mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=["mcp_server.py"],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
    )
)

# Create the ADK Agent
github_card_agent = Agent(
    name="github_card_agent",
    model="gemini-2.5-flash", # Using 2.5-flash as the identifier
    instruction=SYSTEM_INSTRUCTION,
    tools=[mcp_toolset]
)

if __name__ == "__main__":
    # Example usage for testing
    async def main():
        response = await github_card_agent.run("Generate a card for torvalds")
        print(response.text)

    import asyncio
    asyncio.run(main())
