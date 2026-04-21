"""
rag/chunking.py
===============
Owns all document loading and chunking logic.
Called by ingest.py — not used at query time.
"""

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict

from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import FOLDER_CATEGORY_MAP


# ═══════════════════════════════════════════════════════════════════════════════
# Metadata extractors
# ═══════════════════════════════════════════════════════════════════════════════

def _category_from_path(file_path: Path, base_dir: Path) -> str:
    """
    ACL category from the sub-folder name inside the temp download directory.

    <tmp>/knowledge_base/...  →  "kb"
    <tmp>/incidents/...       →  "incidents"
    <tmp>/policies/...        →  "policies"
    <tmp>/employee_data/...   →  "employee_data"
    """
    try:
        relative = file_path.relative_to(base_dir)
        folder   = relative.parts[0] if len(relative.parts) > 1 else "general"
        return FOLDER_CATEGORY_MAP.get(folder, folder)
    except ValueError:
        return "kb"


def _short_name(file_path: Path) -> str:
    """
    Human-readable citation label from filename.
    'kb_password_reset_guide.txt'  →  'Password Reset Guide'
    'INC001_mfa_bypass.pdf'        →  'Inc001 Mfa Bypass'
    """
    stem  = file_path.stem
    clean = stem.replace("kb_", "").replace("_", " ").title()
    return clean


def _extract_kb_id(file_path: Path) -> str:
    """
    Extracts a structured article ID from the filename if present.

    'kb_013_github_setup.txt'  →  'KB-013'
    'INC001_mfa_bypass.pdf'    →  'INC-001'
    'KB013_some_doc.md'        →  'KB-013'
    'random_doc.pdf'           →  ''   (no ID found)
    """
    stem    = file_path.stem.upper()
    # Match INC001, INC-001, KB013, KB-013, POL-05, etc.
    pattern = r'\b(INC|KB|POL|HR|IT|LOG)[_-]?(\d{2,4})\b'
    match   = re.search(pattern, stem)
    if match:
        return f"{match.group(1)}-{match.group(2).lstrip('0').zfill(3)}"
    return ""


def _extract_severity(file_path: Path, category: str) -> str:
    """
    Extracts incident severity from the filename if present.
    Only meaningful for the 'incidents' category.

    'INC001_P1_mfa_bypass.pdf'  →  'P1'
    'INC002_p2_lockout.txt'     →  'P2'
    'anything_else.txt'         →  ''
    """
    if category != "incidents":
        return ""
    stem  = file_path.stem.upper()
    match = re.search(r'\b(P[1-4])\b', stem)
    return match.group(1) if match else ""


def _extract_department(file_path: Path) -> str:
    """
    Infers department from filename keywords.

    'hr_leave_policy.pdf'      →  'HR'
    'it_access_guide.txt'      →  'IT'
    'fin_expense_policy.docx'  →  'Finance'
    'kb_github_setup.md'       →  'Engineering'
    'password_policy.pdf'      →  'IT'  (default for security docs)
    """
    from config import DEPARTMENT_MAPPING
    stem_lower = file_path.stem.lower()
    for keywords, dept in DEPARTMENT_MAPPING.items():
        if any(kw in stem_lower for kw in keywords):
            return dept
    return "General"


# ═══════════════════════════════════════════════════════════════════════════════
# Loader factory
# ═══════════════════════════════════════════════════════════════════════════════

def load_file(file_path: Path) -> List[Document]:
    """
    Picks the correct LangChain loader by file extension.
    Returns an empty list for unsupported formats (silently skipped).
    """
    loaders = {
        ".pdf":  lambda p: PyPDFLoader(str(p)),
        ".pptx": lambda p: UnstructuredPowerPointLoader(str(p)),
        ".xlsx": lambda p: UnstructuredExcelLoader(str(p)),
        ".xls":  lambda p: UnstructuredExcelLoader(str(p)),
        ".md":   lambda p: UnstructuredMarkdownLoader(str(p)),
        ".txt":  lambda p: TextLoader(str(p), encoding="utf-8",
                                      autodetect_encoding=True),
    }
    factory = loaders.get(file_path.suffix.lower())
    if factory is None:
        return []
    try:
        return factory(file_path).load()
    except Exception as e:
        print(f"  ❌  {file_path.name}: {e}")
        return []


# ═══════════════════════════════════════════════════════════════════════════════
# Chunker + metadata injector
# ═══════════════════════════════════════════════════════════════════════════════

def chunk_and_tag(
    file_path: Path,
    raw_docs: List[Document],
    base_dir: Path,
    source_url: str,
) -> List[Document]:
    """
    Splits raw Documents and attaches rich metadata to every chunk.

    Metadata stored in Pinecone per chunk
    ──────────────────────────────────────
    file_name    — original filename                    e.g. "INC001_mfa_bypass.pdf"
    short_name   — clean citation label                 e.g. "Mfa Bypass"
    source_url   — Google Drive webViewLink             e.g. "https://drive.google.com/file/d/.../view"
    category     — ACL partition key                    e.g. "incidents"
    source_type  — file extension without dot           e.g. "pdf"
    kb_id        — structured article reference         e.g. "INC-001" | "KB-013" | ""
    severity     — incident priority (incidents only)   e.g. "P1" | "P2" | ""
    department   — owning team                          e.g. "IT" | "HR" | "Finance"
    ingested_at  — ISO 8601 UTC timestamp               e.g. "2026-04-20T00:00:00Z"
    chunk_index  — position of this chunk in the file   e.g. 0, 1, 2 ...
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        length_function=len,
    )
    chunks     = splitter.split_documents(raw_docs)
    category   = _category_from_path(file_path, base_dir)
    ingested_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    shared_meta = {
        "file_name":   file_path.name,
        "short_name":  _short_name(file_path),
        "source_url":  source_url,
        "category":    category,
        "source_type": file_path.suffix.lower().lstrip("."),
        "kb_id":       _extract_kb_id(file_path),
        "severity":    _extract_severity(file_path, category),
        "department":  _extract_department(file_path),
        "ingested_at": ingested_at,
    }

    for idx, chunk in enumerate(chunks):
        chunk.metadata.update({**shared_meta, "chunk_index": idx})

    return chunks


# ═══════════════════════════════════════════════════════════════════════════════
# Directory processor  (called by ingest.py)
# ═══════════════════════════════════════════════════════════════════════════════

def process_directory(
    base_dir: Path,
    file_url_map: Dict[str, str],
) -> List[Document]:
    """
    Iterates every file in `base_dir`, loads it, chunks it, and tags it.

    Args:
        base_dir:     Root of the temp download directory.
        file_url_map: {local_file_path_str: google_drive_url}

    Returns:
        Flat list of all enriched chunks — ready for embed + upsert.
    """
    all_chunks: List[Document] = []
    total_files = 0

    print(f"📖  Parsing {len(file_url_map)} downloaded files…\n")

    for local_path_str, src_url in file_url_map.items():
        fp = Path(local_path_str)
        if not fp.is_file():
            continue

        raw_docs = load_file(fp)
        if not raw_docs:
            continue

        total_files += 1
        chunks = chunk_and_tag(fp, raw_docs, base_dir, src_url)
        all_chunks.extend(chunks)

        cat    = _category_from_path(fp, base_dir)
        kb_id  = _extract_kb_id(fp)
        label  = f"[{kb_id}] " if kb_id else ""
        print(f"  ✅  {label}{fp.name:<50} [{cat}]  {len(chunks)} chunks")

    print(f"\n📦  {total_files} files  →  {len(all_chunks)} chunks total\n")
    return all_chunks
