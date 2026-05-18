import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from adk import Runner
from adk.services import InMemorySessionService, InMemoryMemoryService
from agent import github_card_agent
from pathlib import Path
import uvicorn

app = FastAPI(title="GitHub Dev Card Generator API")

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup ADK Services and Runner
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()
runner = Runner(
    agent=github_card_agent,
    session_service=session_service,
    memory_service=memory_service
)

# Ensure static directory exists
STATIC_DIR = Path("static/cards")
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Mount static files to serve generated cards
app.mount("/static", StaticFiles(directory="static"), name="static")

class GenerateRequest(BaseModel):
    username: str

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/generate")
async def generate_card(request: GenerateRequest):
    username = request.username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")

    try:
        # Use username as session_id to maintain context for that user
        session_id = f"session_{username}"
        
        # Run the agent through the runner
        response = await runner.run(
            input=f"Generate a dev card for {username}",
            session_id=session_id
        )

        # The agent is instructed to call save_card, which returns the path.
        # We'll return the final text response which should contain the confirmation
        # and we'll also check if the file exists to provide a direct link.
        card_file = STATIC_DIR / f"{username}.html"
        card_url = f"/static/cards/{username}.html" if card_file.exists() else None
        
        card_content = ""
        if card_file.exists():
            with open(card_file, "r", encoding="utf-8") as f:
                card_content = f.read()

        return {
            "status": "success",
            "message": response.text,
            "card_url": card_url,
            "card_html": card_content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/card/{username}")
async def get_card(username: str):
    card_file = STATIC_DIR / f"{username}.html"
    if not card_file.exists():
        raise HTTPException(status_code=404, detail="Card not found")
    
    with open(card_file, "r", encoding="utf-8") as f:
        return {"html": f.read()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
