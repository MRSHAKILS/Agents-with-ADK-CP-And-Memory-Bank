from mcp.server.fastmcp import FastMCP

mcp = FastMCP("GitHubDevCard")

@mcp.tool()
async def fetch_github_stats(username: str) -> str:
    """Fetch GitHub stats for a given username."""
    # TODO: Implement GitHub API call
    return f"Stats for {username}: 100 stars, 50 repos"

if __name__ == "__main__":
    mcp.run()
