from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router as api_router
from backend.db.mongo import connect_to_mongo, close_mongo_connection

app = FastAPI(title="CourseForge AI", description="Agentic AI Hackathon Project")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for hackathon, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to CourseForge AI API"}
