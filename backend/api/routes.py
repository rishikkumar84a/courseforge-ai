from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from pydantic import BaseModel
import uuid
import datetime
from backend.db.mongo import get_db
from backend.agents.orchestrator import run_course_generation

router = APIRouter()

class GenerateRequest(BaseModel):
    topic: str

@router.post("/courses/generate")
async def generate_course(request: GenerateRequest, background_tasks: BackgroundTasks):
    course_id = str(uuid.uuid4())
    
    db = await get_db()
    
    # Initialize course in database
    await db["courses"].insert_one({
        "id": course_id,
        "topic": request.topic,
        "status": "generating",
        "progress": "0",
        "created_at": datetime.datetime.now(datetime.timezone.utc),
        "modules": []
    })
    
    # Task to run the generator and update DB
    def background_generator(topic: str, cid: str):
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Note: run_course_generation is synchronous
            final_data = run_course_generation(topic, cid)
            
            # Format course details maping from agents output to our DB model
            curriculum = final_data.get("curriculum", {})
            
            # For simplicity we save the raw generated modules
            # A more rigorous implementation would map to the Pydantic models
            
            async def update_db():
                db_client = await get_db()
                await db_client["courses"].update_one(
                    {"id": cid},
                    {"$set": {
                        "status": "complete",
                        "progress": "100",
                        "title": curriculum.get("course_title", ""),
                        "description": curriculum.get("description", ""),
                        "modules": curriculum.get("modules", []),
                        "generated_lessons": final_data.get("lessons", []),
                        "generated_quizzes": final_data.get("quizzes", [])
                    }}
                )
            loop.run_until_complete(update_db())
        except Exception as e:
            async def set_failed():
                db_client = await get_db()
                await db_client["courses"].update_one(
                    {"id": cid},
                    {"$set": {
                        "status": "failed",
                        "progress": "0",
                        "error": str(e)
                    }}
                )
            loop.run_until_complete(set_failed())
        finally:
            loop.close()

    background_tasks.add_task(background_generator, request.topic, course_id)
    
    return {"course_id": course_id, "status": "generating"}

@router.get("/courses/{course_id}")
async def get_course(course_id: str):
    db = await get_db()
    course = await db["courses"].find_one({"id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/courses/{course_id}/status")
async def get_course_status(course_id: str):
    db = await get_db()
    course = await db["courses"].find_one({"id": course_id}, {"_id": 0, "status": 1, "progress": 1})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/courses/")
async def list_courses():
    db = await get_db()
    courses = await db["courses"].find({}, {"_id": 0, "id": 1, "topic": 1, "title": 1, "status": 1, "created_at": 1}).to_list(length=100)
    return courses

@router.delete("/courses/{course_id}")
async def delete_course(course_id: str):
    db = await get_db()
    result = await db["courses"].delete_one({"id": course_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"deleted": True}
