"""
main.py — Karan Systems Secure Agentic RAG (CLI)
=================================================
Usage:
    python main.py                          # run full demo
    python main.py --query "..."           # single query (default role: employee)
    python main.py --query "..." --role hr --user EMP103
    python main.py --interactive           # interactive chat mode
"""

import argparse
import json
import os
from datetime import datetime

from agents.orchestrator import KaranAgenticRAG
from config import ROLE_ACCESS


DEMO_QUERIES = [
    ("What is the leave policy at Karan Systems?",
     "employee", "EMP102",
     "General KB lookup — employee role"),

    ("How do I reset my password if I'm locked out?",
     "employee", "EMP102",
     "IT process — password reset"),

    ("How do I request access to a new application in SailPoint?",
     "employee", "EMP104",
     "Access request — SailPoint guide"),

    ("Why did Adam Fox lose access to the Finance App? What was the root cause?",
     "manager", "EMP105",
     "RCA — Incident INC001 (manager role)"),

    ("What caused the account lockout for John Doe on April 14?",
     "it_admin", "IT-ADMIN-01",
     "RCA — Incident INC002 (it_admin role)"),

    ("What is the password policy?",
     "employee", "EMP102",
     "Policy lookup — employee"),

    ("What is the security policy on data classification?",
     "employee", "EMP104",
     "Policy — data classification"),

    ("Walk me through the GitHub SSH key setup process.",
     "developer", "EMP104",
     "KB — GitHub setup (developer role)"),
]


def _print_response(question: str, answer: str, role: str, desc: str):
    print(f"\n{'═' * 65}")
    print(f"  [{desc}]")
    print(f"  Role   : {role}")
    print(f"  Q      : {question}")
    print(f"{'─' * 65}")
    print(f"  A      : {answer}")


def run_demo(rag: KaranAgenticRAG, save_output: bool = True):
    results = []
    print("\n" + "═" * 65)
    print("  KARAN SYSTEMS — SECURE AGENTIC RAG DEMO")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("═" * 65)

    for i, (question, role, user_id, desc) in enumerate(DEMO_QUERIES, 1):
        print(f"\n[{i}/{len(DEMO_QUERIES)}] {desc}")
        answer = rag.query(
            user_query=question,
            chat_history=[],
            role=role,
        )
        _print_response(question, answer, role, desc)
        results.append({
            "demo_case": desc,
            "question": question,
            "role": role,
            "user_id": user_id,
            "answer": answer,
            "timestamp": datetime.now().isoformat(),
        })

        if i < len(DEMO_QUERIES):
            input("\n  ▶  Press ENTER for next query…")

    if save_output:
        out_dir = os.path.join(os.path.dirname(__file__), "outputs")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(
            out_dir,
            f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾  Results saved → {out_path}")

    print(f"\n✅  Demo complete — {len(results)} queries")


def interactive_mode(rag: KaranAgenticRAG):
    print("\n" + "═" * 65)
    print("  KARAN SYSTEMS — INTERACTIVE CHAT")
    print("  Commands: 'quit' | 'role <name>' | 'clear'")
    print("═" * 65)

    role    = "employee"
    history = []
    print(f"\n  Current role: {role}  |  Access: {ROLE_ACCESS[role]}")
    print(f"  Valid roles: {list(ROLE_ACCESS.keys())}\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if user_input.lower() == "clear":
            history = []
            print("  ✅  History cleared.")
            continue
        if user_input.lower().startswith("role "):
            new_role = user_input[5:].strip().lower()
            if new_role in ROLE_ACCESS:
                role    = new_role
                history = []
                print(f"  ✅  Role → {role}  |  Access: {ROLE_ACCESS[role]}")
            else:
                print(f"  ❌  Unknown role. Valid: {list(ROLE_ACCESS.keys())}")
            continue

        answer = rag.query(user_query=user_input, chat_history=history, role=role)
        print(f"\nAgent: {answer}\n")

        history.append({"role": "user",      "content": user_input})
        history.append({"role": "assistant", "content": answer})


def single_query(rag: KaranAgenticRAG, question: str, role: str, user_id: str):
    answer = rag.query(user_query=question, chat_history=[], role=role)
    _print_response(question, answer, role, f"Single query — user: {user_id}")

    out_dir  = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "last_query.json")
    with open(out_path, "w") as f:
        json.dump({"question": question, "answer": answer, "role": role,
                   "user_id": user_id, "timestamp": datetime.now().isoformat()},
                  f, indent=2)
    print(f"\n💾  Saved → {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Karan Systems Secure Agentic RAG")
    parser.add_argument("--query",       type=str,  help="Single question to ask")
    parser.add_argument("--role",        type=str,  default="employee",
                        choices=list(ROLE_ACCESS.keys()),
                        help="User role for ACL enforcement")
    parser.add_argument("--user",        type=str,  default="DEMO_USER",
                        help="Employee ID for audit trail")
    parser.add_argument("--interactive", action="store_true",
                        help="Start interactive chat mode")
    args = parser.parse_args()

    rag = KaranAgenticRAG()

    if args.query:
        single_query(rag, args.query, args.role, args.user)
    elif args.interactive:
        interactive_mode(rag)
    else:
        run_demo(rag)
