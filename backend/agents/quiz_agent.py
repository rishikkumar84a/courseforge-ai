from typing import Dict, Any, List
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class QuizQuestion(BaseModel):
    question: str = Field(description="The multiple choice question")
    options: List[str] = Field(description="Exactly 4 options to choose from")
    correct_answer: str = Field(description="The exact text of the correct option")
    explanation: str = Field(description="Explanation of why the answer is correct")

class ModuleQuiz(BaseModel):
    questions: List[QuizQuestion] = Field(description="List of exactly 5 multiple choice questions")

def run_quiz_agent(module_title: str, module_description: str, research_data: Dict[str, Any]) -> ModuleQuiz:
    """
    Executes the quiz generation phase for a specific module.
    Generates exactly 5 multiple-choice questions based on the module and research data.
    """
    llm = ChatGroq(temperature=0.4, model_name="llama3-70b-8192")
    
    parser = JsonOutputParser(pydantic_object=ModuleQuiz)
    
    prompt = PromptTemplate(
        template="""You are an expert educator and assessment creator.
Generate a multiple-choice quiz for the following module.

Requirements:
- Create EXACTLY 5 multiple-choice questions.
- Each question must have EXACTLY 4 options.
- Indicate the correct answer matching the exact text of one of the options.
- Provide a brief explanation of why the answer is correct.

Module Details:
Title: {module_title}
Description: {module_description}

Context / Research Data:
Topic: {topic}
Key Concepts: {key_concepts}
Facts: {facts}

{format_instructions}""",
        input_variables=["module_title", "module_description", "topic", "key_concepts", "facts"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    
    try:
        structured_data = chain.invoke({
            "module_title": module_title,
            "module_description": module_description,
            "topic": research_data.get("topic", ""),
            "key_concepts": ", ".join(research_data.get("key_concepts", [])),
            "facts": ", ".join(research_data.get("facts", []))
        })
        return ModuleQuiz(**structured_data)
    except Exception as e:
        return ModuleQuiz(questions=[])
