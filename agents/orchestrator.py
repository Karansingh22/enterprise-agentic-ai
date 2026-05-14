"""
agents/orchestrator.py -- Karan Systems Agentic RAG (create_agent API)
======================================================================
Uses the latest `langchain.agents.create_agent` which is backed by
LangGraph under the hood -- no AgentExecutor needed.

Flow per query:
  1. Topic Security Guardrail   -> block off-topic / jailbreak attempts
  2. PII Scrubber               -> mask emails / phone numbers before LLM sees them
  3. Intent Classifier          -> NOISE / REAL / GENERAL
  4. create_agent invocation    -> retrieve + generate with streamed reasoning
"""

import asyncio
import os
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.store.memory import InMemoryStore
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

from config import GEMINI_MODEL, GOOGLE_API_KEY
from prompts.system_prompts import ORCHESTRATOR_SYSTEM_PROMPT
from tools.incident_tools import get_kb_search_tool
from guardrails.safety import check_topic_allowed, scrub_pii


class KaranAgenticRAG:
    """
    Main entry-point for the Karan Systems Agentic RAG.

    Each instance holds:
    - A shared Gemini LLM handle
    - A shared InMemoryStore for cross-turn long-term memory
    """

    def __init__(self):
        print("[INIT]  Initializing Karan Systems Agentic RAG (create_agent with MCP)...")

        # -- LLM ------------------------------------------------
        self.llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.1,
            top_p=0.9,
            convert_system_message_to_human=True,  # required for Gemini
        )
        print(f"   [OK]  LLM: Gemini ({GEMINI_MODEL})")

        # -- Long-term memory store (shared across sessions) ----
        self.store = InMemoryStore()

        print("   [OK]  Agent ready!\n")

    # Keywords that signal the user wants meeting/email functionality
    _MCP_KEYWORDS = {"meeting", "schedule", "invite", "calendar", "send email", "draft email",
                     "send meeting", "book a meeting", "set up a meeting", "draft meeting"}

    @staticmethod
    def _needs_mcp(query: str) -> bool:
        """Fast keyword check — returns True only when the query looks meeting/email-related."""
        q = query.lower()
        return any(kw in q for kw in KaranAgenticRAG._MCP_KEYWORDS)

    async def _aquery(self, safe_query: str, chat_history: list, role: str) -> str:
        """Async internal implementation of query. Only opens an MCP session when needed."""
        # 1. Base tools (always available)
        kb_tool = get_kb_search_tool(role_filter=role)
        all_tools = [kb_tool]

        # 2. Format messages (shared by both paths)
        messages = []
        for msg in chat_history:
            if isinstance(msg, dict):
                messages.append({"role": msg["role"], "content": msg["content"]})
            elif isinstance(msg, (tuple, list)) and len(msg) == 2:
                messages.append({"role": msg[0], "content": msg[1]})
        messages.append({"role": "user", "content": safe_query})

        try:
            if self._needs_mcp(safe_query):
                # --- MCP path: spawn MeetingScheduler only when needed ---
                import sys
                mcp_server_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), "tools", "mcp_server.py"
                )
                client = MultiServerMCPClient({
                    "MeetingScheduler": {
                        "transport": "stdio",
                        "command": sys.executable,
                        "args": [mcp_server_path],
                    }
                })
                async with client.session("MeetingScheduler") as session:
                    mcp_tools = await load_mcp_tools(session)
                    all_tools.extend(mcp_tools)

                    agent = create_agent(
                        model=self.llm,
                        tools=all_tools,
                        system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
                        name="karan_rag_agent",
                        store=self.store,
                    )
                    result = await agent.ainvoke({"messages": messages})
            else:
                # --- KB-only path: no MCP subprocess, no websocket overhead ---
                agent = create_agent(
                    model=self.llm,
                    tools=all_tools,
                    system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
                    name="karan_rag_agent",
                    store=self.store,
                )
                result = await agent.ainvoke({"messages": messages})

            content = result["messages"][-1].content
            if isinstance(content, list):
                text_parts = [p.get("text", "") for p in content if isinstance(p, dict)]
                return "".join(text_parts)
            return str(content)

        except Exception as e:
            return f"Agent execution error (MCP/LLM): {e}"

    # ----------------------------------------------------------
    # Public: main query entry-point
    # ----------------------------------------------------------
    def query(
        self,
        user_query: str,
        chat_history: list,
        role: str,
    ) -> str:
        """
        Process a user query through the full pipeline.
        """
        # -- 1. Topic Guardrail ---------------------------------
        if not check_topic_allowed(user_query):
            return (
                "I'm sorry, I can only assist with Karan Systems IT and HR "
                "topics.  Please rephrase your question."
            )

        # -- 2. PII Scrub ---------------------------------------
        safe_query = scrub_pii(user_query)

        # -- 3. Execute Async Pipeline --------------------------
        return asyncio.run(self._aquery(safe_query, chat_history, role))
