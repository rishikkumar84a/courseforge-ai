import os
from typing import Dict, Any, List
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class ResearchData(BaseModel):
    topic: str = Field(description="The topic being researched")
    key_concepts: List[str] = Field(description="List of core concepts necessary to understand the topic")
    facts: List[str] = Field(description="List of important facts, statistics, or details")
    sources: List[str] = Field(description="List of URLs or source names used")

def run_research_agent(topic: str) -> Dict[str, Any]:
    """
    Executes the research phase for a given topic.
    Extracts key concepts and facts from search results.
    """
    # Prefer Tavily if API key exists, otherwise use DuckDuckGo
    if os.environ.get("TAVILY_API_KEY"):
        search = TavilySearchResults(max_results=5)
        search_results = search.invoke(topic)
    else:
        search = DuckDuckGoSearchResults(max_results=5)
        search_results = search.invoke(topic)

    # Initialize LLM
    llm = ChatGroq(temperature=0.2, model_name="llama3-70b-8192")
    
    parser = JsonOutputParser(pydantic_object=ResearchData)
    
    prompt = PromptTemplate(
        template="You are an expert researcher. Use the following search results to extract key concepts and facts about the topic.\n\nTopic: {topic}\n\nSearch Results: {search_results}\n\n{format_instructions}",
        input_variables=["topic", "search_results"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    
    try:
        structured_data = chain.invoke({"topic": topic, "search_results": str(search_results)})
        return structured_data
    except Exception as e:
        return {
            "topic": topic,
            "key_concepts": [],
            "facts": [f"Error extracting data: {str(e)}"],
            "sources": []
        }
