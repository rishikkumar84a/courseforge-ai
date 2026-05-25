from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
import uuid

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None

class Lesson(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    key_points: List[str]
    order: int

class Module(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    order: int
    lessons: List[Lesson] = Field(default_factory=list)
    quiz: List[QuizQuestion] = Field(default_factory=list)

class Course(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: str
    title: Optional[str] = None
    description: Optional[str] = None
    modules: List[Module] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "generating"  # generating | complete | failed
