import uuid
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class LessonOutline(BaseModel):
    title: str = Field(description="Title of the lesson")
    order: int = Field(description="Order of the lesson within the module (1, 2, 3)")
    description: str = Field(description="Brief outline of what this lesson covers")

class ModuleOutline(BaseModel):
    title: str = Field(description="Title of the module")
    order: int = Field(description="Order of the module (1 to 5)")
    lessons: List[LessonOutline] = Field(description="List of exactly 3 lessons in this module")

class CurriculumOutline(BaseModel):
    course_title: str = Field(description="Engaging title for the course")
    description: str = Field(description="A brief description of the course")
    modules: List[ModuleOutline] = Field(description="List of exactly 5 modules")

def run_curriculum_agent(research_data: Dict[str, Any]) -> CurriculumOutline:
    """
    Executes the curriculum design phase.
    Takes structured research data and generates a full course curriculum outline.
    """
    llm = ChatGroq(temperature=0.3, model_name="llama3-70b-8192")
    
    parser = JsonOutputParser(pydantic_object=CurriculumOutline)
    
    prompt = PromptTemplate(
        template="""You are an expert instructional designer and curriculum architect.
Using the provided research data, design a comprehensive course structure.

Requirements:
- Ensure there are EXACTLY 5 modules.
- Ensure each module contains EXACTLY 3 lessons.
- The content flow should be logical, starting from basics and advancing progressively.

Research Data:
Topic: {topic}
Key Concepts: {key_concepts}
Facts: {facts}

{format_instructions}""",
        input_variables=["topic", "key_concepts", "facts"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    
    try:
        structured_data = chain.invoke({
            "topic": research_data.get("topic", ""),
            "key_concepts": ", ".join(research_data.get("key_concepts", [])),
            "facts": ", ".join(research_data.get("facts", []))
        })
        # Parse into Pydantic model for returning
        return CurriculumOutline(**structured_data)
    except Exception as e:
        # Fallback in case of failure
        return CurriculumOutline(
            course_title=f"Course on {research_data.get('topic', 'Unknown')}",
            description=f"Error generating curriculum: {str(e)}",
            modules=[]
        )
