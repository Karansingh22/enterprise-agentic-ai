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
    initial_sidebar_state="collapsed",
)

# =========================================================
# LOAD CSS
# =========================================================

css_path = os.path.join(os.path.dirname(__file__), "ui", "style.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# =========================================================
# AURORA BACKGROUND
# =========================================================

st.markdown("""
<div class="aurora-bg">
    <div class="aurora aurora1"></div>
    <div class="aurora aurora2"></div>
    <div class="aurora aurora3"></div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_data" not in st.session_state:
    st.session_state.user_data = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1, 1.3, 1])

    with col2:

        st.markdown("""
        <div class="login-wrapper">

            <div class="brand-orb">
                ◆
            </div>

            <div class="brand-title">
                KARAN SYSTEMS
            </div>

            <div class="brand-subtitle">
                AGENTIC RAG COMMAND CENTER
            </div>

        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):

            email = st.text_input(
                "Corporate Email",
                placeholder="you@karansystems.ai"
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

                st.session_state.messages = [
                    {
                        "role": "assistant",
                        "content":
                            f"Hello {record['name']}! "
                            f"I'm your enterprise AI assistant."
                    }
                ]

                st.rerun()

            else:
                st.error("Authentication failed.")

        st.markdown("""
        <div class="security-footer">
            ● End-to-end encrypted · SOC2 compliant · RBAC enforced
        </div>
        """, unsafe_allow_html=True)

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

    st.markdown(f"""
    <div class="sidebar-brand">

        <div class="sidebar-logo">
            ◆
        </div>

        <div>
            <div class="sidebar-title">
                KARAN SYSTEMS
            </div>

            <div class="sidebar-subtitle">
                AGENTIC RAG v2.0
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Workspace")

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("<div class='sidebar-divider'></div>",
                unsafe_allow_html=True)

    st.markdown(f"""
    <div class="user-card">

        <div class="avatar">
            {user['name'][0]}
        </div>

        <div>
            <div class="user-name">
                {user['name']}
            </div>

            <div class="user-role">
                {role.replace("_", " ").title()}
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Access")

    access = ROLE_ACCESS.get(role, [])

    for a in access:
        st.markdown(
            f"<div class='access-tag'>{a}</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⏻ Sign Out", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.user_data = None
        st.session_state.messages = []

        st.rerun()

# =========================================================
# HERO SECTION
# =========================================================

st.markdown(f"""
<div class="hero-wrapper">

    <div class="hero-badge">
        AGENTIC RAG COMMAND CENTER
    </div>

    <div class="hero-title">
        Welcome back, {user['name']}
    </div>

    <div class="hero-subtitle">
        Enterprise intelligence orchestration powered by
        autonomous multi-agent reasoning systems.
    </div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# TOP METRICS
# =========================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">ACTIVE AGENTS</div>
        <div class="metric-value">12</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">VECTOR INDEX</div>
        <div class="metric-value">4.2M</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">LATENCY</div>
        <div class="metric-value">128ms</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# LOAD AGENT
# =========================================================

@st.cache_resource
def load_agent():
    return KaranAgenticRAG()

agent = load_agent()

# =========================================================
# CHAT HISTORY
# =========================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================================================
# INPUT
# =========================================================

prompt = st.chat_input(
    "Ask about incidents, policies, HR, infrastructure..."
)

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

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

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })