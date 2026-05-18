# GitHub Dev Card Generator

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-orange)

An intelligent agentic application that dynamically generates beautiful, personalized GitHub developer cards. It analyzes your GitHub profile using Google's Gemini 2.5 Flash LLM, infers your "developer vibe," and creates a highly styled, shareable HTML card.

## 🚀 Features

- **Intelligent Profile Analysis**: Uses Gemini 2.5 Flash to infer your top skills, developer vibe, and "fun facts" based on your public repositories.
- **Dynamic Theming**: Automatically assigns a visually stunning theme (`hacker`, `builder`, `researcher`, `designer`, `open-source-hero`) based on your coding activity.
- **Agentic Workflows**: Powered by Google ADK and orchestrated through MCP (Model Context Protocol).
- **Fast & Modern UI**: Standalone React frontend styled with Tailwind CSS, backed by a blazing-fast FastAPI server.

## 🛠️ Tech Stack

- **Orchestration:** [Google ADK](https://github.com/google/agent-development-kit)
- **Tools:** MCP ([FastMCP](https://github.com/fastmcp/fastmcp))
- **LLM:** Gemini 2.5 Flash
- **Backend:** Python, FastAPI
- **Frontend:** React, HTML, TailwindCSS
- **Deployment:** Google Cloud Run (Dockerized)

## 📁 Project Structure

```text
.
├── backend/
│   ├── agent.py         # Google ADK agent definition & orchestration
│   ├── main.py          # FastAPI application entry point
│   ├── mcp_server.py    # FastMCP server with tools for GitHub scraping & generation
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile       # Backend container definition
├── frontend/
│   ├── index.html       # React frontend with Tailwind styling
│   └── Dockerfile       # Frontend container definition
├── docker-compose.yml   # Multi-container local execution
└── GEMINI.md            # Engineering standards and plan
```

## ⚙️ Engineering Standards

- **Dependency Management:** Maintained with `uv` for speed and deterministic resolution.
- **Code Quality:** Clean, modular Python code following idiomatic patterns for both FastAPI and React.

## 🏃‍♂️ Getting Started

### Prerequisites
- Docker and Docker Compose
- A Google Gemini API Key
- [uv](https://github.com/astral-sh/uv) (for local development without Docker)

### Environment Setup

1. Copy the example `.env` file to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Add your Gemini API key to the newly created `.env` file:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

### Running with Docker Compose (Recommended)

You can quickly spin up both the frontend and backend using Docker Compose:
```bash
docker-compose up --build
```
- **Frontend UI:** Available at `http://localhost:8080`
- **Backend API:** Available at `http://localhost:8000`

### Running Locally (Without Docker)

1. Navigate to the `backend` directory.
2. Install dependencies using `uv`:
   ```bash
   uv pip install -r requirements.txt
   ```
3. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Run the FastMCP server standalone (if you want to test the tools directly):
   ```bash
   python mcp_server.py
   ```
5. Simply open `frontend/index.html` in your favorite web browser or host it via a local static server.

## 🤖 How it Works

1. **Input**: User enters a GitHub username in the React frontend.
2. **Scraping**: `mcp_server.py` utilizes the `scrape_github` tool to retrieve the user's repositories and profile stats via the GitHub REST API.
3. **Analysis**: The `analyze_profile` tool leverages Gemini 2.5 Flash to read the profile data, determining the user's top skills, developer vibe, and an appropriate visual theme.
4. **Generation**: `generate_card_html` assembles a stunning Tailwind-styled HTML snippet injected with the user's personalized data.
5. **Storage**: The finalized card is saved locally via `save_card` for sharing or downloading.

---
*Built with ❤️ using Google ADK and Gemini 2.5 Flash.*
