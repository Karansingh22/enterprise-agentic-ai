import os
from dotenv import load_dotenv

load_dotenv()

# -- Identity -------------------------------------------------
COMPANY = "Karan Systems Pvt. Ltd."

# -- API Keys -------------------------------------------------
GOOGLE_API_KEY   = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


# -- Model Configuration --------------------------------------
GEMINI_MODEL       = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_EMBED_MODEL = "models/gemini-embedding-001" # Forced to bypass any deprecated secrets

# -- Vector Store Configuration -------------------------------
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "karan-systems-data")
PINECONE_NAMESPACE  = os.getenv("PINECONE_NAMESPACE", "")   # leave blank for default namespace
TOP_K_RETRIEVAL     = int(os.getenv("TOP_K", "5"))
TOP_K               = TOP_K_RETRIEVAL                        # alias used in some modules

# -- Google Drive Ingestion Source ----------------------------
# The top-level Google Drive folder that holds all KB data.
# In production this would be GCS_BUCKET / S3_BUCKET / AZURE_CONTAINER.
GDRIVE_FOLDER_ID = os.getenv(
    "GDRIVE_FOLDER_ID", "1aBwWDLyGUnbClgNnIAeWzG7JTIJ7_TRz"
)
GDRIVE_FOLDER_URL = f"https://drive.google.com/drive/folders/{GDRIVE_FOLDER_ID}"

# -- Role-Based Access Control Matrix ------------------------
# Values map to the 'category' metadata field stored in Pinecone per chunk.
ROLE_ACCESS = {
    "employee":  ["kb", "policies"],
    "manager":   ["kb", "policies", "incidents"],
    "hr":        ["kb", "policies", "incidents", "employee_data"],
    "it_admin":  ["kb", "policies", "incidents", "employee_data", "logs"],
    "developer": ["kb", "policies"],
}

# -- Category tag -> Pinecone metadata 'category' value -------
# Sub-folder names inside the Drive / data/ directory are used as category tags.
FOLDER_CATEGORY_MAP = {
    "knowledge_base":  "kb",
    "policies":        "policies",
    "incidents":       "incidents",
    "employee_data":   "employee_data",
    "logs":            "logs",
}

# -- Mock Authentication Database -----------------------------
MOCK_USERS = {
    "singh@karansystem.com": {
        "password": "karan",
        "role":    "it_admin",
        "user_id": "EMP_001",
        "name":    "Karan Singh",
    },
    "employee@karansystems.in": {
        "password": "password123",
        "role":    "employee",
        "user_id": "EMP_002",
        "name":    "Test Employee",
    },
}

# -- Department Mapping for chunking --------------------------
DEPARTMENT_MAPPING = {
    ("hr_", "leave", "salary", "onboard", "payroll", "employee"): "HR",
    ("it_", "password", "vpn", "access", "network", "sailpoint",
     "mfa", "ldap", "sso", "github", "ssh"):                       "IT",
    ("fin_", "finance", "expense", "invoice", "budget"):           "Finance",
    ("sec_", "security", "compliance", "audit", "gdpr", "iso"):    "Security",
    ("dev_", "github", "deploy", "ci_", "cd_", "pipeline"):        "Engineering",
}