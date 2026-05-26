from typing import Dict, Any, List
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class LessonContent(BaseModel):
    content: str = Field(description="The main text of the lesson (300-500 words)")
    key_points: List[str] = Field(description="List of 3-5 key points or takeaways")
    examples: List[str] = Field(description="List of practical examples illustrating the concepts")
    summary: str = Field(description="A brief summary of the lesson")

def run_content_agent(lesson_title: str, lesson_description: str, research_data: Dict[str, Any]) -> LessonContent:
    """
    Executes the content generation phase for a single lesson.
    Returns the comprehensive content including key points and summary.
    """
    llm = ChatGroq(temperature=0.4, model_name="llama3-70b-8192")
    
    parser = JsonOutputParser(pydantic_object=LessonContent)
    
    prompt = PromptTemplate(
        template="""You are an expert educator and course creator.
Write comprehensive instructional content for the following lesson.

Requirements:
- The main content should be around 300-500 words.
- Explain concepts clearly using an engaging, accessible tone.
- Incorporate practical examples to illustrate the points.
- Provide 3-5 key takeaways and a brief summary.

Lesson Details:
Title: {lesson_title}
Description: {lesson_description}

Context / Research Data:
Topic: {topic}
Key Concepts: {key_concepts}
Facts: {facts}

{format_instructions}""",
        input_variables=["lesson_title", "lesson_description", "topic", "key_concepts", "facts"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    
    try:
        structured_data = chain.invoke({
            "lesson_title": lesson_title,
            "lesson_description": lesson_description,
            "topic": research_data.get("topic", ""),
            "key_concepts": ", ".join(research_data.get("key_concepts", [])),
            "facts": ", ".join(research_data.get("facts", []))
        })
        return LessonContent(**structured_data)
    except Exception as e:
        return LessonContent(
            content=f"Error generating content: {str(e)}",
            key_points=[],
            examples=[],
            summary="Error"
        )
