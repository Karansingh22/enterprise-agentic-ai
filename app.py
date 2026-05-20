import streamlit as st
import os
from config import COMPANY, ROLE_ACCESS, MOCK_USERS
from agents.orchestrator import KaranAgenticRAG

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title=f"{COMPANY} — Agentic RAG",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# LOAD CSS & TAILWIND
# =========================================================

# Load Tailwind CSS CDN directly in the header using st.html
st.html("<script src='https://cdn.tailwindcss.com'></script>")

css_path = os.path.join(os.path.dirname(__file__), "ui", "style.css")

with open(css_path) as f:
    st.html(f"<style>{f.read()}</style>")

# =========================================================
# AURORA BACKGROUND
# =========================================================

st.html("""<div class="aurora-bg"><div class="aurora aurora1"></div><div class="aurora aurora2"></div><div class="aurora aurora3"></div></div>""")

# =========================================================
# CHAT DATABASE HELPERS
# =========================================================

import json

CHATS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools", "chats.json")

def load_chats():
    if os.path.exists(CHATS_FILE):
        try:
            with open(CHATS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_chats(chats):
    os.makedirs(os.path.dirname(CHATS_FILE), exist_ok=True)
    with open(CHATS_FILE, "w") as f:
        json.dump(chats, f, indent=4)

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_data" not in st.session_state:
    st.session_state.user_data = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1, 1.3, 1])

    with col2:
        st.html("""<div class="login-wrapper"><div class="brand-orb">◆</div><div class="brand-title">KARAN SYSTEMS</div><div class="brand-subtitle">AGENTIC RAG COMMAND CENTER</div></div>""")

        with st.form("login_form"):
            email = st.text_input(
                "Corporate Email",
                placeholder="singh@karansystem.com"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter secure password"
            )

            submit = st.form_submit_button("AUTHENTICATE →")

            if submit:
                record = MOCK_USERS.get(email.strip())

                if record and record["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.user_data = record
                    st.session_state.messages = []
                    st.session_state.current_session_id = None
                    st.rerun()
                else:
                    st.error("Authentication failed.")

        st.html("""<div class="security-footer">● End-to-end encrypted · SOC2 compliant · RBAC enforced</div>""")

        st.stop()

# =========================================================
# MAIN APP
# =========================================================

user = st.session_state.user_data
role = user["role"]

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    # Use standard Streamlit button but style it to look like the design
    if st.button("NEW CHAT", use_container_width=True):
        st.session_state.current_session_id = None
        st.session_state.messages = []
        st.rerun()

    # Dynamic recent chats list
    chats = load_chats()
    user_chats = [c for c in chats.values() if c.get("user_email") == user["email"]]
    user_chats.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    st.html("""<div class="sidebar-menu"><div class="menu-label">WORKSPACE</div><div class="menu-label mt-4">RECENT CHATS</div></div>""")

    if not user_chats:
        st.sidebar.html("<div style='padding: 0 16px; color: #64748b; font-size: 12px; font-style: italic;'>No active chats</div>")
    else:
        for chat_item in user_chats:
            is_active = (chat_item["id"] == st.session_state.current_session_id)
            btn_label = f"👉 {chat_item['title']}" if is_active else f"💬 {chat_item['title']}"
            if st.button(btn_label, key=f"btn_{chat_item['id']}", use_container_width=True):
                st.session_state.current_session_id = chat_item["id"]
                st.session_state.messages = chat_item["messages"]
                st.rerun()

    # Display user profile at the bottom of sidebar
    st.html(f"""<div class="sidebar-bottom"><div class="user-profile"><div class="avatar-img"><img src="https://ui-avatars.com/api/?name={user['name'].replace(' ', '+')}&background=00ffe5&color=030712" alt="User"></div><div class="user-info"><div class="user-name">{user['name'].upper()}</div><div class="user-role">{role.replace("_", " ").upper()}</div></div><div class="user-menu-icon">⌄</div></div></div>""")

# =========================================================
# MAIN APP HEADER
# =========================================================

st.html(f"""<div class="command-deck-header"><div>COMMAND DECK <span class="ml-4 text-xs font-semibold px-2 py-1 bg-white/5 border border-white/5 rounded-full text-slate-400">Welcome back, {user['name']} · {role.replace('_', ' ').lower()}</span></div><div class="deck-icons"><span class="icon">◫</span><span class="icon">⋮</span></div></div>""")

# =========================================================
# LOAD AGENT
# =========================================================

@st.cache_resource
def load_agent():
    return KaranAgenticRAG()

agent = load_agent()

# =========================================================
# TABS NAVIGATION
# =========================================================

tab_chat, tab_calendar = st.tabs(["💬 Chat Deck", "📅 Schedule Deck"])

# ── Chat Deck Tab ──
with tab_chat:
    # CHAT HISTORY
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown(f"Hello {user['name']}! I'm your enterprise AI assistant. How can I help you today?")
    else:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # INPUT
    prompt = st.chat_input("Type a message...")

    if prompt:
        chats = load_chats()

        # If starting a new session
        if not st.session_state.current_session_id:
            import secrets
            from datetime import datetime
            session_id = secrets.token_hex(8)
            st.session_state.current_session_id = session_id
            title = prompt[:25] + ("..." if len(prompt) > 25 else "")
            chats[session_id] = {
                "id": session_id,
                "user_email": user["email"],
                "title": title.upper(),
                "messages": [],
                "timestamp": datetime.now().isoformat()
            }

        session = chats[st.session_state.current_session_id]

        # Append user message
        session["messages"].append({
            "role": "user",
            "content": prompt
        })
        st.session_state.messages = session["messages"]

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Running multi-agent reasoning..."):
                response = agent.query(
                    user_query=prompt,
                    chat_history=st.session_state.messages[:-1],
                    role=role,
                )
                st.markdown(response)

        # Append assistant response
        session["messages"].append({
            "role": "assistant",
            "content": response
        })

        from datetime import datetime
        session["timestamp"] = datetime.now().isoformat()

        save_chats(chats)
        st.session_state.messages = session["messages"]
        st.rerun()

# ── Schedule Deck Tab ──
with tab_calendar:
    st.html("<h3 style='color: white; margin-top: 15px; font-weight: bold;'>Scheduled Meetings & Invitations</h3>")

    from tools.mcp_server import load_drafts, generate_ics_content, MAIL_SENDER
    try:
        drafts = load_drafts()
        if not drafts:
            st.info("No scheduled meetings found.")
        else:
            for m_id, meeting in reversed(list(drafts.items())):
                is_sent = meeting["status"] == "sent"
                badge = "🟢 Scheduled & Sent" if is_sent else "🟡 Drafted (Pending Approval)"

                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {meeting['subject']}")
                        st.caption(f"Status: {badge}")
                    with col2:
                        st.markdown(f"⏰ {meeting['date_time']}")
                        st.caption(f"Duration: {meeting['duration_minutes']} mins")

                    st.markdown(f"**Agenda:** {meeting['agenda']}")

                    # Format participant list with code tags to prevent blue underlines
                    participants_formatted = ", ".join([f"`{p}`" for p in meeting['participants']])
                    st.markdown(f"**Participants:** {participants_formatted}")

                    ics_data = generate_ics_content(meeting, MAIL_SENDER)
                    st.download_button(
                        label="📥 Add to Calendar (.ics)",
                        data=ics_data,
                        file_name=f"invite-{m_id}.ics",
                        mime="text/calendar",
                        key=f"dl_{m_id}"
                    )
    except Exception as e:
        st.error(f"Failed to load calendar events: {str(e)}")