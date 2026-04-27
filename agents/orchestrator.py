"""
agents/orchestrator.py — Karan Systems Agentic RAG (create_agent API)
======================================================================
Uses the latest `langchain.agents.create_agent` which is backed by
LangGraph under the hood — no AgentExecutor needed.

Flow per query:
  1. Topic Security Guardrail   → block off-topic / jailbreak attempts
  2. PII Scrubber               → mask emails / phone numbers before LLM sees them
  3. Intent Classifier          → NOISE / REAL / GENERAL
  4. create_agent invocation    → retrieve + generate with streamed reasoning
"""

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.store.memory import InMemoryStore

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
    - A factory that creates a fully-configured create_agent graph
      dynamically per user role (so ACL filter is always correct)
    """

    def __init__(self):
        print("🔧  Initializing Karan Systems Agentic RAG (create_agent)...")

        # ── LLM ────────────────────────────────────────────────
        self.llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.1,
            top_p=0.9,
            convert_system_message_to_human=True,  # required for Gemini
        )
        print(f"   ✅  LLM: Gemini ({GEMINI_MODEL})")

        # ── Long-term memory store (shared across sessions) ────
        # In production: swap InMemoryStore for PostgresStore or RedisStore.
        self.store = InMemoryStore()

        print("   ✅  Agent ready!\n")

    # ──────────────────────────────────────────────────────────
    # Internal: build a fresh agent graph for the given role
    # ──────────────────────────────────────────────────────────
    def _build_agent(self, role: str):
        """
        Creates a LangGraph-backed agent using create_agent.

        The KB search tool is built with the user's ACL role baked into
        its closure so it cannot be tampered with by the LLM.
        """
        kb_tool = get_kb_search_tool(role_filter=role)

        agent = create_agent(
            model=self.llm,
            tools=[kb_tool],
            system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
            name="karan_rag_agent",
            store=self.store,       # enable long-term memory
        )
        return agent

    # ──────────────────────────────────────────────────────────
    # Public: main query entry-point
    # ──────────────────────────────────────────────────────────
    def query(
        self,
        user_query: str,
        chat_history: list,
        role: str,
    ) -> str:
        """
        Process a user query through the full pipeline.

        Args:
            user_query:   Raw text from the user.
            chat_history: List of {"role": "user"/"assistant", "content": str}
            role:         Authenticated user role (e.g. "employee", "it_admin")

        Returns:
            str — the agent's final answer.
        """

        # ── 1. Topic Guardrail ─────────────────────────────────
        if not check_topic_allowed(user_query):
            return (
                "I'm sorry, I can only assist with Karan Systems IT and HR "
                "topics.  Please rephrase your question."
            )

        # ── 2. PII Scrub ───────────────────────────────────────
        safe_query = scrub_pii(user_query)

        # ── 3. Skip Intent Classification to save LLM calls ────
        contextualized_query = safe_query

        # ── 4. Build agent with correct ACL role ───────────────
        agent = self._build_agent(role=role)

        # ── 5. Build message list  (history + current turn) ───
        messages = []
        for msg in chat_history:
            # Accept both dict style and tuple style history
            if isinstance(msg, dict):
                messages.append({"role": msg["role"], "content": msg["content"]})
            elif isinstance(msg, (tuple, list)) and len(msg) == 2:
                messages.append({"role": msg[0], "content": msg[1]})

        messages.append({"role": "user", "content": contextualized_query})

        # ── 6. Invoke create_agent ────────────────────────────
        try:
            result = agent.invoke({"messages": messages})
            # create_agent returns a LangGraph state dict;
            # the final answer is always the last message.
            return result["messages"][-1].content

        except Exception as e:
            return f"Agent error: {e}"
