import uuid
from typing import Dict, Any, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# Import the agents
from backend.agents.research_agent import run_research_agent
from backend.agents.curriculum_agent import run_curriculum_agent
from backend.agents.content_agent import run_content_agent
from backend.agents.quiz_agent import run_quiz_agent

class AgentState(TypedDict):
    topic: str
    course_id: str
    research_data: Dict[str, Any]
    curriculum: Dict[str, Any]
    lessons_content: List[Dict[str, Any]]
    quizzes: List[Dict[str, Any]]
    final_output: Dict[str, Any]
    status: str

def node_research(state: AgentState) -> Dict[str, Any]:
    print(f"[{state['course_id']}] Running Research Agent for: {state['topic']}")
    data = run_research_agent(state["topic"])
    return {"research_data": data, "status": "research_completed"}

def node_curriculum(state: AgentState) -> Dict[str, Any]:
    print(f"[{state['course_id']}] Running Curriculum Agent")
    curriculum = run_curriculum_agent(state["research_data"])
    return {"curriculum": curriculum.model_dump(), "status": "curriculum_completed"}

def node_content_and_quiz(state: AgentState) -> Dict[str, Any]:
    print(f"[{state['course_id']}] Running Content and Quiz Agents")
    # For a real implementation, these would run in parallel nodes,
    # but we can execute them iteratively here for simplicity
    modules = state["curriculum"].get("modules", [])
    
    all_lessons = []
    all_quizzes = []
    
    for mod in modules:
        # Run quiz agent for the module
        quiz_data = run_quiz_agent(mod["title"], "Module covering " + mod["title"], state["research_data"])
        all_quizzes.append({
            "module_title": mod["title"],
            "quiz": quiz_data.model_dump()
        })
        
        # Run content agent for each lesson
        for lesson in mod.get("lessons", []):
            content_data = run_content_agent(
                lesson["title"], 
                lesson["description"], 
                state["research_data"]
            )
            all_lessons.append({
                "module_title": mod["title"],
                "lesson_title": lesson["title"],
                "content": content_data.model_dump()
            })
            
    return {"lessons_content": all_lessons, "quizzes": all_quizzes, "status": "content_quiz_completed"}

def node_aggregator(state: AgentState) -> Dict[str, Any]:
    print(f"[{state['course_id']}] Aggregating final course data")
    final_course = {
        "course_id": state["course_id"],
        "topic": state["topic"],
        "curriculum": state["curriculum"],
        "lessons": state["lessons_content"],
        "quizzes": state["quizzes"]
    }
    # In a full app, we would save to MongoDB here or via API
    return {"final_output": final_course, "status": "complete"}

def build_orchestrator_graph():
    builder = StateGraph(AgentState)
    
    builder.add_node("research", node_research)
    builder.add_node("curriculum", node_curriculum)
    builder.add_node("content_quiz", node_content_and_quiz)
    builder.add_node("aggregator", node_aggregator)
    
    builder.add_edge(START, "research")
    builder.add_edge("research", "curriculum")
    builder.add_edge("curriculum", "content_quiz")
    builder.add_edge("content_quiz", "aggregator")
    builder.add_edge("aggregator", END)
    
    return builder.compile()

def run_course_generation(topic: str, course_id: str = None) -> Dict[str, Any]:
    graph = build_orchestrator_graph()
    course_id = course_id or str(uuid.uuid4())
    
    initial_state = {
        "topic": topic,
        "course_id": course_id,
        "research_data": {},
        "curriculum": {},
        "lessons_content": [],
        "quizzes": [],
        "final_output": {},
        "status": "started"
    }
    
    final_state = graph.invoke(initial_state)
    return final_state["final_output"]
