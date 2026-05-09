"""
ingest.py -- Karan Systems Ingestion Pipeline (Orchestrator)
============================================================
This file ONLY handles:
  1. DOWNLOAD  -> Pull folder from Google Drive into a temp directory
  2. CLEANUP   -> Delete temp directory when done (or on error)

All parsing, chunking, embedding, and uploading is delegated to:
  - rag/chunking.py   -> load + split + attach metadata
  - rag/retrieval.py  -> embed + upsert to Pinecone

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


# ===============================================================================
# STEP 1 -- Download from Google Drive
# ===============================================================================

def download_from_gdrive(folder_id: str, dest_dir: str) -> Dict[str, str]:
    """
    Downloads the entire public Google Drive folder into `dest_dir`.

    Returns:
        {local_file_path_str: google_drive_file_view_url}
        Used by rag/chunking.py to attach source_url metadata per chunk.

    Uses gdown's skip_download to pre-fetch per-file IDs, then downloads.
    """
    try:
        import gdown
    except ImportError:
        print("ERROR: gdown not installed. Run: pip install gdown")
        sys.exit(1)

    # -- Step 1: List all files to get per-file Drive IDs -----------------
    file_url_map: Dict[str, str] = {}   # relative_path -> Drive view URL
    try:
        file_list = gdown.download_folder(
            id=folder_id, skip_download=True, quiet=True,
        )
        for entry in file_list:
            fid = getattr(entry, "id", "")
            fpath = getattr(entry, "path", "")
            if fid and fpath:
                file_url_map[fpath] = f"https://drive.google.com/file/d/{fid}/view"
        print(f"    Resolved {len(file_url_map)} per-file Drive URLs.\n")
    except Exception as e:
        print(f"    Could not list per-file URLs ({e}). Falling back to folder URL.\n")

    # -- Step 2: Download all files ---------------------------------------
    print(f"    Downloading Google Drive folder -> {dest_dir}")
    print(f"    {GDRIVE_FOLDER_URL}\n")

    try:
        gdown.download_folder(
            id=folder_id,
            output=dest_dir,
            quiet=False,
        )
    except Exception as e:
        print(f"    gdown failed: {e}")
        print("    Falling back to local 'data/' directory for CI/CD.")
        local_data_dir = Path(__file__).resolve().parent.parent / "data"
        if local_data_dir.exists():
            shutil.copytree(local_data_dir, dest_dir, dirs_exist_ok=True)
            print("    Copied local data directory for ingestion.")
        else:
            raise RuntimeError(f"Local fallback 'data/' not found. Gdown error was: {e}")

    # -- Step 3: Map local paths to their Drive URLs ----------------------
    result: Dict[str, str] = {}
    for local_path in Path(dest_dir).rglob("*"):
        if local_path.is_file():
            # Match by relative path within the download dir
            rel = str(local_path.relative_to(dest_dir))
            url = file_url_map.get(rel, "")
            # Also try matching with forward slashes
            if not url:
                rel_fwd = rel.replace("\\", "/")
                for key, val in file_url_map.items():
                    if key.replace("\\", "/") == rel_fwd:
                        url = val
                        break
            # Also try matching by filename only (last resort before folder URL)
            if not url:
                fname = local_path.name
                for key, val in file_url_map.items():
                    if key.endswith(fname) or key.endswith("/" + fname) or key.endswith("\\" + fname):
                        url = val
                        break
            if not url:
                url = GDRIVE_FOLDER_URL
                print(f"      No per-file URL for: {rel} -- using folder URL")
            result[str(local_path)] = url

    print(f"\n    {len(result)} files ready for processing.\n")
    return result


# ===============================================================================
# Pinecone index management
# ===============================================================================

def ensure_pinecone_index(pc: Pinecone) -> None:
    existing = [idx.name for idx in pc.list_indexes()]
    if PINECONE_INDEX_NAME not in existing:
        print(f"    Creating index '{PINECONE_INDEX_NAME}' (dim=3072, cosine)...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=3072,         # Gemini gemini-embedding-001 output dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        print("       Index created.\n")
    else:
        print(f"    Index '{PINECONE_INDEX_NAME}' exists.\n")


# ===============================================================================
# MAIN PIPELINE
# ===============================================================================

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
            print(f"    Deleting index '{PINECONE_INDEX_NAME}'...")
            pc.delete_index(PINECONE_INDEX_NAME)
            print("    Deleted.\n")

    ensure_pinecone_index(pc)

    # Temp dir is created here and deleted in the finally block -- always.
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
            print(f"    Temp dir deleted: {tmp_dir}")

    print("\n    Ingestion complete!")
    print(f"    Index : {PINECONE_INDEX_NAME}")


# ===============================================================================
# CLI
# ===============================================================================

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
