from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="GitHub Dev Card Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "GitHub Dev Card Generator API is running"}

@app.post("/generate")
async def generate_card(username: str):
    # Logic to trigger ADK agent
    return {"status": "success", "username": username}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
