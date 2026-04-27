"""
ingest.py — Karan Systems Ingestion Pipeline (Orchestrator)
============================================================
This file ONLY handles:
  1. DOWNLOAD  → Pull folder from Google Drive into a temp directory
  2. CLEANUP   → Delete temp directory when done (or on error)

All parsing, chunking, embedding, and uploading is delegated to:
  - rag/chunking.py   → load + split + attach metadata
  - rag/retrieval.py  → embed + upsert to Pinecone

Usage:
  python ingest.py           # download from Drive, ingest, cleanup
  python ingest.py --clear   # wipe Pinecone index first, then ingest
"""

import os
import sys
import shutil
import tempfile
import argparse
from pathlib import Path
from typing import Dict

from pinecone import Pinecone, ServerlessSpec

from config import (
    GOOGLE_API_KEY,
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    GDRIVE_FOLDER_ID,
    GDRIVE_FOLDER_URL,
)
from rag.chunking import process_directory
from rag.retrieval import upload_to_pinecone


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Download from Google Drive
# ═══════════════════════════════════════════════════════════════════════════════

def download_from_gdrive(folder_id: str, dest_dir: str) -> Dict[str, str]:
    """
    Downloads the entire public Google Drive folder into `dest_dir`.

    Returns:
        {local_file_path_str: google_drive_webViewLink}
        Used by rag/chunking.py to attach source_url metadata per chunk.

    Tries the Drive API first for per-file URLs.
    Falls back to the folder URL if the API is unavailable.
    """
    try:
        import gdown
    except ImportError:
        print("❌  gdown not installed. Run: uv add gdown")
        sys.exit(1)

    # ── Try to collect per-file Drive URLs ───────────────────────────────
    file_url_map: Dict[str, str] = {}   # filename → webViewLink
    try:
        from googleapiclient.discovery import build
        service = build(
            "drive", "v3",
            developerKey=GOOGLE_API_KEY,
            cache_discovery=False,
        )
        _collect_drive_urls(service, folder_id, file_url_map)
        print(f"ℹ️   Drive API: resolved {len(file_url_map)} file URLs.\n")
    except Exception as e:
        print(f"ℹ️   Drive API unavailable ({e}). Falling back to folder URL.\n")

    # ── Download all files ────────────────────────────────────────────────
    print(f"📥  Downloading Google Drive folder → {dest_dir}")
    print(f"    {GDRIVE_FOLDER_URL}\n")

    gdown.download_folder(
        id=folder_id,
        output=dest_dir,
        quiet=False,
        use_cookies=False,
    )

    # ── Map local paths to their Drive URLs ──────────────────────────────
    result: Dict[str, str] = {}
    for local_path in Path(dest_dir).rglob("*"):
        if local_path.is_file():
            url = file_url_map.get(local_path.name, GDRIVE_FOLDER_URL)
            result[str(local_path)] = url

    print(f"\n✅  {len(result)} files ready for processing.\n")
    return result


def _collect_drive_urls(service, folder_id: str,
                        acc: Dict[str, str]) -> None:
    """Recursively walks a Drive folder collecting filename → webViewLink."""
    page_token = None
    while True:
        resp = service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, mimeType, webViewLink)",
            pageToken=page_token,
        ).execute()

        for f in resp.get("files", []):
            if f["mimeType"] == "application/vnd.google-apps.folder":
                _collect_drive_urls(service, f["id"], acc)
            else:
                acc[f["name"]] = f.get("webViewLink", GDRIVE_FOLDER_URL)

        page_token = resp.get("nextPageToken")
        if not page_token:
            break


# ═══════════════════════════════════════════════════════════════════════════════
# Pinecone index management
# ═══════════════════════════════════════════════════════════════════════════════

def ensure_pinecone_index(pc: Pinecone) -> None:
    existing = [idx.name for idx in pc.list_indexes()]
    if PINECONE_INDEX_NAME not in existing:
        print(f"🆕  Creating index '{PINECONE_INDEX_NAME}' (dim=768, cosine)…")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=768,          # Gemini embedding-001 output dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        print("   ✅  Index created.\n")
    else:
        print(f"✅  Index '{PINECONE_INDEX_NAME}' exists.\n")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

def run_ingestion(clear_index: bool = False) -> None:
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY missing from .env")
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY missing from .env")
    if not GDRIVE_FOLDER_ID:
        raise ValueError("GDRIVE_FOLDER_ID missing from .env / config.py")

    pc = Pinecone(api_key=PINECONE_API_KEY)

    if clear_index:
        if PINECONE_INDEX_NAME in [idx.name for idx in pc.list_indexes()]:
            print(f"⚠️   Deleting index '{PINECONE_INDEX_NAME}'…")
            pc.delete_index(PINECONE_INDEX_NAME)
            print("    Deleted.\n")

    ensure_pinecone_index(pc)

    # Temp dir is created here and deleted in the finally block — always.
    tmp_dir = tempfile.mkdtemp(prefix="karan_rag_ingest_")

    try:
        # 1. Download from Drive
        file_url_map = download_from_gdrive(GDRIVE_FOLDER_ID, tmp_dir)

        # 2 + 3. Parse + Chunk  (rag/chunking.py)
        chunks = process_directory(Path(tmp_dir), file_url_map)

        # 4 + 5. Embed + Upsert  (rag/retrieval.py)
        upload_to_pinecone(chunks)

    finally:
        # 6. Always delete temp files
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
            print(f"🗑️   Temp dir deleted: {tmp_dir}")

    print("\n🎉  Ingestion complete!")
    print(f"    Index : {PINECONE_INDEX_NAME}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ingest Google Drive docs into Pinecone"
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Delete and recreate the Pinecone index before ingesting",
    )
    run_ingestion(clear_index=parser.parse_args().clear)
