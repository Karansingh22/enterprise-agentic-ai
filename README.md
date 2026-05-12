# 🤖 Karan Systems — Enterprise Agentic RAG
**Stack:** LangChain Agents + Google Gemini + Pinecone Vector Database + Streamlit Cloud  
**Company:** Karan Systems Pvt. Ltd.  

---

## 🚀 What This Project Is & The Problem It Solves

**The Problem:** Modern IT and HR departments spend countless hours answering repetitive questions, triaging simple "noise" alerts (like transient outages), and manually sifting through policy documents and raw logs. 
When a real incident occurs, routing it effectively, retrieving relevant root cause analyses (RCA), and accessing specific internal KB articles often involves navigating a fragmented data landscape, wasting valuable time.

**The Solution:** This project is an **Enterprise Agentic Retrieval-Augmented Generation (RAG) System**. It acts as an autonomous tier-1 and tier-2 robotic assistant for the organization.
- **Intelligent Triage:** The Multi-Agent logic automatically classifies queries into "Noise" or "Real" issues. If it's a noise issue, it handles it instantly. If it's a real issue, it queries the internal Knowledge Base.
- **Enterprise Guardrails:** The system enforces strict Role-Based Access Control (ACL) at the vector database level, meaning employees can never access HR salary data or IT-admin raw logs. Furthermore, the system masks Personally Identifiable Information (PII) before it touches any LLM.
- **Clean Citations:** Using intelligent metadata chunking, the assistant provides clean, short names for KB articles instead of exposing messy URLs or hallucinating facts.

**Future Vision (MCP Integration):** In the future, this system will integrate full Model Context Protocol (MCP) tools to allow the agentic system to take real actions within the organization: programmatically sending emails, scheduling meetings via Outlook/calendar plugins, and generating automated end-of-week incident reports directly to management channels.

---

## 📁 Enterprise Project Structure

```text
karan_rag/
├── rag/                                   
│   ├── chunking.py                       ← Structure-Aware chunking in temp/memory (PPT, Excel, MD, OCR)
│   ├── embedding.py                      ← Gemini embeddings generator
│   └── retrieval.py                      ← Pinecone Database Layer integration
├── tools/                                 
│   └── incident_tools.py                 ← Tools for Pinecone retrieval & Incident routing logic
├── agents/                                
│   ├── classifier.py                     ← Agent responsible for classifying query intent (Noise vs Real)
│   └── orchestrator.py                   ← Reasoning Agent for executing tools and human-like greetings
├── prompts/                               
│   └── system_prompts.py                 ← Centralized system context, personas, and instructions
├── guardrails/                            
│   ├── acl.py                            ← Access Control Lists (Role-Based metadata filtering for DB search)
│   └── safety.py                         ← PII scrubbing and Topic Blocking rules
├── data/                                 ← Legacy offline data dump zone (Google Drive sync)
├── app.py                                ← Main Streamlit Interface
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone / Download the project

```bash
# Or download the zip and extract
cd karan_rag
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Gemini API Key

```bash
cp .env.example .env
# Edit .env — paste your Google AI Studio API key
# Get one free at: https://aistudio.google.com/app/apikey
```

Your `.env` file:
```
GOOGLE_API_KEY=AIzaSy...your_key_here
GEMINI_MODEL=gemini-2.0-flash
GEMINI_EMBEDDING_MODEL=models/text-embedding-004
```

### 4. Ingest all documents into ChromaDB

```bash
python ingest.py
```

This will:
- Load all source files (MD, TXT, XLSX, DOCX, PPTX)
- Split into overlapping chunks (800 chars, 150 overlap)
- Generate Gemini embeddings for each chunk
- Store everything in ChromaDB (persisted in `chroma_db/`)

To re-ingest from scratch:
```bash
python ingest.py --reset
```

### 5. Run the demo

```bash
# Full demo — 10 queries across all roles and query types
python main.py

# Single query
python main.py --query "What is the leave policy?" --role employee --user EMP101

# Interactive chat
python main.py --interactive
```

---

## 🔐 Role-Based Access Control (ACL)

| Role       | KB | Policies | Incidents | Logs | Employee Data |
|------------|:--:|:--------:|:---------:|:----:|:-------------:|
| employee   | ✅ | ✅       | ❌        | ❌   | ❌            |
| developer  | ✅ | ✅       | ❌        | ❌   | ❌            |
| manager    | ✅ | ✅       | ✅        | ❌   | ❌            |
| hr         | ✅ | ✅       | ✅        | ❌   | ✅            |
| it_admin   | ✅ | ✅       | ✅        | ✅   | ✅            |

ACL is enforced at the **ChromaDB query filter level** — blocked roles never see restricted chunks.

---

## 🧠 Query Types

| Type      | Trigger Keywords                          | Example                                       |
|-----------|-------------------------------------------|-----------------------------------------------|
| general   | (default)                                 | "What is the leave policy?"                   |
| rca       | why, root cause, incident, INC, caused    | "Why did Adam lose access?"                   |
| sensitive | salary, compensation, PII, bank account   | "What is Adam's salary?"                      |
| access    | request access, SailPoint, entitlement    | "How do I get GitHub access?"                 |
| policy    | policy, compliance, rule, requirement     | "What is the password policy?"                |

---

## 📤 Response Format

Every query returns a structured dict:

```json
{
  "question":          "Why did Adam lose access?",
  "answer":            "**Issue:** Adam Fox (EMP101) lost access...\n**Root Cause:** ...",
  "type":              "rca",
  "sources": [
    {
      "file_name":    "incident_cases.txt",
      "source_type":  "incidents",
      "kb_id":        "",
      "access_level": "manager",
      "department":   "IT"
    }
  ],
  "confidence":        0.87,
  "access_level_used": "manager",
  "user_id":           "EMP105",
  "chunks_retrieved":  5,
  "access_denied":     false,
  "timestamp":         "2026-04-15T10:30:00",
  "rca": {
    "incident_id":   "INC001",
    "root_cause":    "Incorrect offboarding trigger...",
    "resolution":    "Group membership restored...",
    "source_files":  ["incident_cases.txt"]
  }
}
```

---

## 🔧 Customisation

### Add new documents
Drop any `.md`, `.txt`, `.xlsx`, `.docx`, or `.pptx` file into the appropriate `data/` subfolder and re-run `python ingest.py --reset`.

### Add a new role
Edit `config.py`:
```python
ROLE_ACCESS["auditor"] = ["kb", "policies", "incidents", "logs"]
```

### Switch Gemini model
In `.env`:
```
GEMINI_MODEL=gemini-1.5-pro    # higher quality, slower
GEMINI_MODEL=gemini-1.5-flash  # faster, cheaper (default)
```

---

## 📊 Data Overview

| Folder          | Files | Content                                        | Access Level |
|-----------------|-------|------------------------------------------------|-------------|
| knowledge_base  | 13    | Leave, VPN, SailPoint, GitHub, Onboarding, etc | employee+   |
| incidents       | 2     | INC001, INC002, INC003 + triage guide          | manager+    |
| policies        | 2     | Security policy, Access policy                 | employee+   |
| employee_data   | 2     | Employee roster (XLSX) + profiles (DOCX)       | hr only     |
| logs            | 1     | AD/SailPoint/AzureAD access logs (April 2026)  | it_admin    |
| pptx            | 1     | Onboarding presentation                        | employee+   |

---

## 💡 Example Queries to Try

```bash
# General
"What is the Karan Systems leave policy?"
"How do I set up VPN on my MacBook?"
"What happens during offboarding?"

# RCA
"Why did Adam Fox lose access to the Finance App?"
"What caused the INC001 incident?"
"Why was John Doe's account locked on April 14?"

# Access
"How do I request SailPoint access?"
"How do I join the GitHub org and set up SSH keys?"
"What is the approval workflow for privileged access?"

# Policy
"What are the password policy requirements?"
"What data classification levels does Karan Systems use?"
"What are the consequences of a security policy violation?"

# Sensitive (HR only)
"What is Adam Fox's salary?"
"Show me the employee roster with salaries."
```

---

*Karan Systems Pvt. Ltd. — Powered by AI. Built for People.*
