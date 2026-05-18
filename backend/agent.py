import os
import sys
from adk import Agent
from adk.toolsets import McpToolset
from dotenv import load_dotenv

load_dotenv()

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
    command=sys.executable,
    args=["mcp_server.py"],
    cwd=os.path.dirname(os.path.abspath(__file__))
)

# Create the ADK Agent
github_card_agent = Agent(
    name="github_card_agent",
    model="gemini-2.0-flash", # Using 2.0-flash as the identifier
    instructions=SYSTEM_INSTRUCTION,
    toolsets=[mcp_toolset]
)

if __name__ == "__main__":
    # Example usage for testing
    async def main():
        response = await github_card_agent.run("Generate a card for torvalds")
        print(response.text)

    import asyncio
    asyncio.run(main())
