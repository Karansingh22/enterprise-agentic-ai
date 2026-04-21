"""
tools/incident_tools.py
=======================
LangChain tool factory for knowledge-base retrieval.

The tool is built dynamically per request so the ACL role-filter is
captured in the closure — the LLM cannot override or inspect it.
"""

from langchain.tools import tool
from rag.retrieval import get_retriever


def get_kb_search_tool(role_filter: str):
    """
    Returns a LangChain @tool with its ACL role-filter baked in.

    The tool is re-created per authenticated request.
    The LLM only sees the `query` argument.
    """

    @tool
    def search_internal_knowledge_base(query: str) -> str:
        """
        Search the Karan Systems internal knowledge base, incident reports,
        and policy documents.  Always call this tool before answering any
        factual question.  Pass a concise, keyword-rich search query.

        Returns formatted context with source citations including
        the original document URL so the user can open the source directly.
        """
        retriever = get_retriever(role_filter=role_filter)
        docs      = retriever.invoke(query)

        if not docs:
            return (
                "No matching documents found in the Karan Systems knowledge base. "
                "Manual investigation may be required."
            )

        lines = []
        for doc in docs:
            # ── Pull all metadata fields ──────────────────────────────
            short_name  = doc.metadata.get("short_name",  "Unknown Document")
            source_url  = doc.metadata.get("source_url",  "")
            category    = doc.metadata.get("category",    "")
            kb_id       = doc.metadata.get("kb_id",       "")
            severity    = doc.metadata.get("severity",    "")
            department  = doc.metadata.get("department",  "")
            ingested_at = doc.metadata.get("ingested_at", "")
            content     = doc.page_content.strip()

            # ── Build citation header ─────────────────────────────────
            # Format: **[INC-001] Mfa Bypass** (incidents · IT · P1)
            # with a clickable link if source_url is available
            ref_label = f"[{kb_id}] {short_name}" if kb_id else short_name
            tags = " · ".join(filter(None, [category, department, severity]))

            if source_url:
                header = f"**[{ref_label}]({source_url})**"
            else:
                header = f"**{ref_label}**"

            if tags:
                header += f"  _({tags})_"

            if ingested_at:
                header += f"  `indexed: {ingested_at[:10]}`"

            lines.append(f"{header}\n{content}")

        return "\n\n---\n\n".join(lines)

    return search_internal_knowledge_base
