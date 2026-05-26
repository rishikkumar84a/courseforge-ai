# CourseForge AI
Drop a topic. Get a full course. Powered by autonomous AI agents.

## Tech Stack
- Agent Orchestration: LangGraph (Python)
- LLM: Groq API (llama3-70b-8192)
- Web Search: Tavily API
- Backend: FastAPI (Python 3.11)
- Frontend: React + Tailwind CSS
- Database: MongoDB Atlas
- Containerization: Docker + docker-compose
- Testing: pytest (backend), Vitest (frontend)

## Features
- Autonomous multi-agent course generation pipeline
- Web research for topic validation
- Curriculum design (5 modules, 3 lessons each)
- Lesson content generation
- Quiz creation with MCQs
- Progress tracking
- Course storage and retrieval

## Architecture Diagram
```
USER INPUT: "topic"
      |
      v
 [Orchestrator Agent]
      |
      |-----> [Research Agent]
      |           - Web search
      |           - Source collection
      |
      |-----> [Curriculum Agent]
      |           - Course structure design
      |
      |-----> [Content Agent]
      |           - Lesson writing
      |
      |-----> [Quiz Agent]
      |           - MCQ generation
      |
      v
 [Aggregator]
      - Combine outputs
      - Save to MongoDB
      - Return course JSON
```

## Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & docker-compose
- Groq API key
- Tavily API key
- MongoDB Atlas URI

## Environment Variables
Create a `.env` file (see `.env.example` for all required keys)

## Installation & Local Setup
### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Docker
```bash
docker-compose up
```

## Running Tests
### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

## API Documentation
### POST /api/courses/generate
Generate a new course
- Body: `{ "topic": "string" }`
- Response: `{ "course_id": "uuid", "status": "generating" }`

### GET /api/courses/{course_id}
Get full course details

### GET /api/courses/{course_id}/status
Get course generation status and progress

### GET /api/courses/
List all generated courses

### DELETE /api/courses/{course_id}
Delete a course
