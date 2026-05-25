# PRD — CourseForge AI
## Agentic AI Hackathon (Unstop) | Deadline: May 25, 11:59 PM IST

---

## 1. PRODUCT OVERVIEW

**Product Name:** CourseForge AI
**Tagline:** Drop a topic. Get a full course. Powered by autonomous AI agents.
**Type:** Agentic AI Application
**Built for:** AI Hackathon for Builders (Unstop/BreakoutAI)

### What it does
CourseForge AI takes a single topic input from the user (e.g., "Machine Learning for Beginners")
and autonomously deploys a team of AI agents that:
1. Research the topic across the web
2. Architect a curriculum with modules and lessons
3. Write lesson content for each module
4. Generate quiz questions and answers
5. Package everything as a structured, downloadable course

This is NOT a chatbot. It is a multi-agent autonomous pipeline.

---

## 2. TARGET USER

- Students who want structured self-learning material fast
- Teachers who need ready-made course outlines
- EdTech builders prototyping curriculum tools

---

## 3. TECH STACK

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph (Python) |
| LLM | Groq API (llama3-70b-8192) — fast and free tier |
| Web Search | Tavily API (free tier) or DuckDuckGo tool |
| Backend | FastAPI (Python 3.11) |
| Frontend | React + Tailwind CSS |
| Database | MongoDB Atlas (free tier) |
| Containerization | Docker + docker-compose |
| Testing | pytest (backend), Vitest (frontend) |
| Version Control | GitHub (strict DevOps — see GITHUB_DEVOPS_RULES.md) |

---

## 4. AGENT ARCHITECTURE

```
USER INPUT: "topic"
      |
      v
 [Orchestrator Agent]
      |
      |-----> [Research Agent]
      |           - Uses Tavily/DuckDuckGo to search web
      |           - Collects 5-10 relevant sources
      |           - Extracts key concepts and facts
      |           - Returns: structured_research_data
      |
      |-----> [Curriculum Agent]  (runs after Research)
      |           - Takes research data
      |           - Designs course structure: 5 modules, 3 lessons each
      |           - Returns: curriculum_outline (JSON)
      |
      |-----> [Content Agent]  (runs after Curriculum)
      |           - For each lesson, writes 300-500 word content
      |           - Includes examples, key points, summary
      |           - Returns: lesson_content_array
      |
      |-----> [Quiz Agent]  (runs in parallel with Content)
      |           - For each module, generates 5 MCQ questions
      |           - With 4 options and correct answer
      |           - Returns: quiz_data_array
      |
      v
 [Aggregator]
      - Combines all outputs
      - Saves to MongoDB
      - Returns complete course JSON
```

---

## 5. DATA MODELS

### Course
```json
{
  "id": "uuid",
  "topic": "string",
  "title": "string",
  "description": "string",
  "modules": [Module],
  "created_at": "datetime",
  "status": "generating | complete | failed"
}
```

### Module
```json
{
  "id": "uuid",
  "course_id": "uuid",
  "title": "string",
  "order": "int",
  "lessons": [Lesson],
  "quiz": [QuizQuestion]
}
```

### Lesson
```json
{
  "id": "uuid",
  "module_id": "uuid",
  "title": "string",
  "content": "string",
  "key_points": ["string"],
  "order": "int"
}
```

### QuizQuestion
```json
{
  "question": "string",
  "options": ["A", "B", "C", "D"],
  "correct_answer": "A|B|C|D",
  "explanation": "string"
}
```

---

## 6. API ENDPOINTS (FastAPI)

```
POST /api/courses/generate
  Body: { "topic": "string" }
  Response: { "course_id": "uuid", "status": "generating" }

GET /api/courses/{course_id}
  Response: Full Course object with all modules and lessons

GET /api/courses/{course_id}/status
  Response: { "status": "generating|complete|failed", "progress": "0-100" }

GET /api/courses/
  Response: List of all generated courses

DELETE /api/courses/{course_id}
  Response: { "deleted": true }
```

---

## 7. FRONTEND PAGES

### Page 1 — Home (/)
- Input box: "Enter a topic to generate a course"
- Generate button
- Shows loading state with agent progress (Research → Curriculum → Content → Quiz)
- Shows recent courses list

### Page 2 — Course View (/course/:id)
- Course title and description
- Sidebar: module navigation
- Main area: lesson content
- Quiz section at end of each module
- Progress tracker

### Page 3 — Loading/Progress (/generating/:id)
- Real-time agent status (SSE or polling)
- Shows which agent is currently running
- Progress bar

---

## 8. ENVIRONMENT VARIABLES (.env.example)

```
GROQ_API_KEY=
TAVILY_API_KEY=
MONGODB_URI=
FRONTEND_URL=http://localhost:3000
PORT=8000
```

---

## 9. PROJECT FOLDER STRUCTURE

```
courseforge-ai/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py
│   │   ├── research_agent.py
│   │   ├── curriculum_agent.py
│   │   ├── content_agent.py
│   │   └── quiz_agent.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models/
│   │   └── course.py
│   ├── db/
│   │   └── mongo.py
│   ├── tests/
│   │   ├── test_agents.py
│   │   ├── test_routes.py
│   │   └── test_models.py
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── App.jsx
│   ├── package.json
│   └── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 10. GITHUB DEVOPS WORKFLOW FOR THIS PROJECT

Follow GITHUB_DEVOPS_RULES.md strictly. Feature branches for this project:

```
feature/project-scaffold         → Folder structure, README, .env.example
feature/mongodb-connection        → DB setup and models
feature/research-agent            → Research Agent implementation
feature/curriculum-agent          → Curriculum Agent
feature/content-agent             → Content Agent
feature/quiz-agent                → Quiz Agent
feature/orchestrator              → Orchestrator + LangGraph graph
feature/fastapi-routes            → All API endpoints
feature/frontend-home             → Home page UI
feature/frontend-course-view      → Course view page
feature/frontend-progress         → Progress/loading page
feature/docker-setup              → Dockerfile + docker-compose
feature/ci-github-actions         → CI pipeline
```

Each branch → PR → @github-copilot review → merge → next branch.

---

## 11. UNIT TESTS REQUIRED

### Backend (pytest)
```python
# tests/test_agents.py
def test_research_agent_returns_data()
def test_curriculum_agent_returns_5_modules()
def test_content_agent_returns_lesson_content()
def test_quiz_agent_returns_5_questions_per_module()
def test_orchestrator_runs_full_pipeline()

# tests/test_routes.py
def test_generate_endpoint_returns_course_id()
def test_get_course_returns_full_course()
def test_delete_course_removes_from_db()
```

### Frontend (Vitest)
```javascript
// src/tests/
test('Home renders input and button')
test('Progress page shows agent steps')
test('Course page renders modules and lessons')
```

---

## 12. DEMO VIDEO GUIDE (Loom — record this)

1. Open the app
2. Type "Introduction to Machine Learning"
3. Click Generate
4. Show the progress screen — agents working
5. Course appears — navigate through modules
6. Show a quiz question
7. Show GitHub repo with clean commit history and merged PRs

Keep video under 3 minutes.

---

## 13. SUBMISSION CHECKLIST

```
[ ] GitHub repo is PUBLIC
[ ] README has all sections (see GITHUB_DEVOPS_RULES.md)
[ ] Demo video uploaded to Loom or YouTube (public/unlisted)
[ ] docker-compose up works cleanly
[ ] All tests pass
[ ] Submit at: https://forms.gle/deDQ7BRT4yHx9nY28
[ ] Deadline: May 25, 11:59 PM IST
```
