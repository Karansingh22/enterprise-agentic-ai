from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts.system_prompts import CLASSIFIER_SYSTEM_PROMPT
from config import GEMINI_MODEL, GOOGLE_API_KEY

def classify_intent(query: str) -> str:
    """
    Analyzes the user query and strictly outputs 'NOISE', 'REAL', or 'GENERAL'.
    Uses a very low temperature for deterministic routing.
    Implemented as a zero-tool agent for easy expansion in Phase 2.
    """
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.0
    )
    
    agent = create_agent(
        model=llm,
        tools=[],
        system_prompt=CLASSIFIER_SYSTEM_PROMPT,
        name="intent_classifier"
    )
    
    try:
        result = agent.invoke({"messages": [("user", query)]})
        output = result["messages"][-1].content.strip().upper()
        
        # Fallback safeguard
        if "NOISE" in output: return "NOISE"
        if "REAL" in output: return "REAL"
        return "GENERAL"
        
    except Exception as e:
        print(f"Classification failed: {e}")
        return "GENERAL"
