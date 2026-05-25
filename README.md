# CourseForge AI
Drop a topic. Get a full course. Powered by autonomous AI agents.

## Tech Stack
- **Agent Orchestration**: LangGraph (Python)
- **LLM**: Groq API (llama3-70b-8192)
- **Web Search**: Tavily API / DuckDuckGo tool
- **Backend**: FastAPI (Python 3.11)
- **Frontend**: React + Tailwind CSS
- **Database**: MongoDB Atlas
- **Containerization**: Docker + docker-compose
- **Testing**: pytest (backend), Vitest (frontend)

## Features
- Autonomous multi-agent pipeline
- Dynamic curriculum generation
- Real-time generation progress tracking
- Quizzes and learning modules
- Automated content writing based on deep web research

## Architecture Diagram 
`
USER INPUT -> [Orchestrator Agent]
                   |
                   |--> [Research Agent] -> [Curriculum Agent] -> [Content Agent] & [Quiz Agent] -> Aggregator -> MongoDB
`

## Prerequisites
- Node.js > 18
- Python > 3.11
- Docker & docker-compose
- MongoDB Atlas cluster
- Groq API Key
- Tavily API Key

## Environment Variables
See .env.example for all required keys. You will need:
- GROQ_API_KEY
- TAVILY_API_KEY
- MONGODB_URI
- FRONTEND_URL
- PORT

## Installation & Local Setup
1. Clone the repo
2. Copy .env.example to .env and fill the values.
3. Run docker-compose up --build

## Running Tests
- Backend: cd backend && pytest
- Frontend: cd frontend && npm run test

## API Documentation 
Available at http://localhost:8000/docs when the backend is running.

## Demo Video Link
(To be added)

## Live Deployment URL
(To be added)
