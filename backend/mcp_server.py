import os
import httpx
import json
import asyncio
from typing import Dict, List
from mcp.server.fastmcp import FastMCP
from google import genai
from google.genai import types
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("GitHubDevCard")

GITHUB_API_URL = "https://api.github.com"
client_genai = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

@mcp.tool()
async def scrape_github(username: str) -> Dict:
    """Fetch GitHub stats for a given username using the REST API."""
    async with httpx.AsyncClient() as client:
        # Profile info
        user_resp = await client.get(f"{GITHUB_API_URL}/users/{username}")
        if user_resp.status_code != 200:
            return {"error": f"User {username} not found"}
        user_data = user_resp.json()

        # Repos info
        repos_resp = await client.get(f"{GITHUB_API_URL}/users/{username}/repos?sort=updated&per_page=30")
        repos_data = repos_resp.json() if repos_resp.status_code == 200 else []

        # Process top 6 repos (sorted by stars)
        top_repos = sorted(repos_data, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:6]
        processed_repos = [
            {
                "name": r.get("name"),
                "stars": r.get("stargazers_count"),
                "language": r.get("language"),
                "description": r.get("description")
            } for r in top_repos
        ]

        # Aggregate languages
        languages = {}
        for r in repos_data:
            lang = r.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
        
        sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)

        return {
            "name": user_data.get("name") or username,
            "bio": user_data.get("bio"),
            "location": user_data.get("location"),
            "public_repos": user_data.get("public_repos"),
            "followers": user_data.get("followers"),
            "avatar_url": user_data.get("avatar_url"),
            "top_repos": processed_repos,
            "most_used_languages": [l[0] for l in sorted_langs[:5]]
        }

@mcp.tool()
async def analyze_profile(github_data: Dict) -> Dict:
    """Analyze GitHub profile using Gemini 2.5 Flash to determine dev vibe and theme."""
    prompt = f"""
    Analyze this GitHub profile data and return a JSON object with:
    1. developer_vibe: A 1-sentence witty personality description.
    2. top_skills: A list of the top 3 technical skills.
    3. fun_fact: A clever observation inferred from their repositories.
    4. card_theme: Choose exactly one from: "hacker", "builder", "researcher", "designer", "open-source-hero".

    Data: {json.dumps(github_data)}
    """
    
    response = client_genai.models.generate_content(
        model="gemini-2.0-flash", # Using 2.0-flash as stable identifier
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    return json.loads(response.text)

@mcp.tool()
async def generate_card_html(username: str, github_data: Dict, analysis: Dict) -> str:
    """Generate a self-contained HTML string for a beautiful dev card based on analysis."""
    theme = analysis.get("card_theme", "builder")
    
    themes = {
        "hacker": "bg-gray-900 text-green-400 border-green-500",
        "builder": "bg-blue-900 text-white border-blue-400",
        "researcher": "bg-indigo-100 text-indigo-900 border-indigo-400",
        "designer": "bg-pink-50 text-pink-600 border-pink-300",
        "open-source-hero": "bg-orange-500 text-white border-white"
    }
    
    theme_class = themes.get(theme, themes["builder"])
    
    repos_html = "".join([
        f'<div class="repo-card p-2 border rounded mb-2 bg-black/20">'
        f'<div class="font-bold">{r["name"]}</div>'
        f'<div class="text-xs opacity-80">{r["description"] or ""}</div>'
        f'<div class="text-xs mt-1">⭐ {r["stars"]} | {r["language"]}</div>'
        f'</div>'
        for r in github_data.get("top_repos", [])[:3]
    ])
    
    skills_html = "".join([
        f'<span class="px-2 py-1 rounded-full bg-white/20 text-xs mr-1">{s}</span>'
        for s in analysis.get("top_skills", [])
    ])

    html = f"""
    <div class="p-6 rounded-2xl border-4 shadow-2xl max-w-sm font-sans {theme_class}">
        <div class="flex items-center mb-4">
            <img src="{github_data.get('avatar_url')}" class="w-16 h-16 rounded-full border-2 border-current mr-4 shadow-lg" />
            <div>
                <h2 class="text-xl font-bold">{github_data.get('name')}</h2>
                <p class="text-sm opacity-90">@{username}</p>
            </div>
        </div>
        <p class="italic mb-4 text-sm">"{analysis.get('developer_vibe')}"</p>
        <div class="mb-4">
            <div class="text-xs uppercase font-bold mb-1">Top Skills</div>
            <div class="flex flex-wrap">{skills_html}</div>
        </div>
        <div class="grid grid-cols-2 gap-4 mb-4 text-center">
            <div class="bg-black/10 p-2 rounded">
                <div class="text-lg font-bold">{github_data.get('public_repos')}</div>
                <div class="text-[10px] uppercase">Repos</div>
            </div>
            <div class="bg-black/10 p-2 rounded">
                <div class="text-lg font-bold">{github_data.get('followers')}</div>
                <div class="text-[10px] uppercase">Followers</div>
            </div>
        </div>
        <div class="mb-4">
            <div class="text-xs uppercase font-bold mb-2 text-center">Featured Projects</div>
            {repos_html}
        </div>
        <div class="text-[10px] opacity-70 text-center">
            💡 {analysis.get('fun_fact')}
        </div>
    </div>
    """
    return html

@mcp.tool()
async def save_card(username: str, html: str) -> str:
    """Save the HTML card to a static directory and return the relative path."""
    static_dir = Path("static/cards")
    static_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = static_dir / f"{username}.html"
    
    # Wrap in full HTML boilerplate for standalone viewing
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>body {{ display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #0f172a; }}</style>
    </head>
    <body>
        {html}
    </body>
    </html>
    """
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    return f"/static/cards/{username}.html"

if __name__ == "__main__":
    mcp.run()
