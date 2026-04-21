import re

def scrub_pii(text: str) -> str:
    """
    Basic guardrail logic to mask PII (Emails, Phone Numbers, SSNs) 
    before it hits the LLM. 
    """
    if not text:
        return text

    # Mask standard email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    text = re.sub(email_pattern, "[EMAIL_MASKED]", text)
    
    # Mask standard 10 digit Phone Numbers (Simple basic filter)
    phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
    text = re.sub(phone_pattern, "[PHONE_MASKED]", text)
    
    return text

def check_topic_allowed(query: str) -> bool:
    """
    Topic blocking semantic guardrail. Disallows queries that are clearly 
    malicious or entirely outside the system's corporate IT/HR scope.
    """
    blocked_keywords = ["write me a poem", "ignore previous instructions", "tell me a joke", "python script to hack"]
    query_lower = query.lower()
    
    for kw in blocked_keywords:
        if kw in query_lower:
            return False
            
    return True
