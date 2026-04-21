from config import ROLE_ACCESS
from typing import List

def get_allowed_departments_for_role(role: str) -> List[str]:
    """
    Returns the allowed 'category' or 'department' chunks for a given role based
    on the centralized ROLE_ACCESS matrix.
    
    This list is passed specifically as a Pinecone vector metadata filter:
        filter={"category": {"$in": allowed_departments}}
        
    If the role is totally unrecognized, it defaults to public/general policies only.
    """
    
    role = role.lower().strip()
    
    # Return the mapped permissions, or safe fallback for unrecognized roles
    if role in ROLE_ACCESS:
        return ROLE_ACCESS[role]
    else:
        # Failsafe: Only allow generic policies if an unknown role bypasses authentication somehow.
        print(f"⚠️ Warning: Unrecognized role '{role}' attempting access. Defaulting to safe fallback.")
        return ["policies"]
