import streamlit as st
from config import COMPANY, ROLE_ACCESS, MOCK_USERS
from agents.orchestrator import KaranAgenticRAG

# -- Page config --------------------------------------------------------------
st.set_page_config(
    page_title=f"{COMPANY} — Agentic RAG",
    page_icon="◆",
    layout="wide",
)

# Load CSS
import os
css_path = os.path.join(os.path.dirname(__file__), "ui", "style.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -- Session-state init --------------------------------------------------------
_SESSION_VERSION = 4  # bump when MOCK_USERS or auth logic changes

for key, default in {
    "logged_in": False,
    "user_data": None,
    "messages":  None,
    "session_version": 0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Auto-invalidate stale sessions from previous config versions
if st.session_state.get("session_version", 0) != _SESSION_VERSION:
    st.session_state["logged_in"] = False
    st.session_state["user_data"] = None
    st.session_state["messages"] = None
    st.session_state["session_version"] = _SESSION_VERSION

# ===============================================================================
# 1. AUTHENTICATION — Quantum Glass Login
# ===============================================================================
if not st.session_state["logged_in"]:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Animated AI nucleus orb
        st.markdown("""
        <div style="display:flex; justify-content:center; margin-bottom:8px; margin-top:40px;">
            <div style="
                width: 80px; height: 80px;
                border-radius: 50%;
                background: linear-gradient(135deg, #06d6a0, #3b82f6, #8b5cf6);
                background-size: 300% 300%;
                animation: orbPulse 4s ease-in-out infinite, orbGradient 6s ease-in-out infinite;
                box-shadow: 0 0 40px rgba(6, 214, 160, 0.25), 0 0 80px rgba(139, 92, 246, 0.15);
                display: flex; align-items: center; justify-content: center;
            ">
                <span style="font-size: 2rem; filter: brightness(2);">◆</span>
            </div>
        </div>
        <style>
            @keyframes orbPulse {
                0%, 100% { transform: scale(1); box-shadow: 0 0 40px rgba(6,214,160,0.25), 0 0 80px rgba(139,92,246,0.15); }
                50% { transform: scale(1.08); box-shadow: 0 0 60px rgba(6,214,160,0.35), 0 0 120px rgba(139,92,246,0.2); }
            }
            @keyframes orbGradient {
                0%, 100% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
            }
        </style>
        """, unsafe_allow_html=True)

        st.title(f"{COMPANY}")

        st.markdown("""
        <p style='
            color: #7b8ba3;
            font-size: 1rem;
            margin-bottom: 2rem;
            text-align: center;
            font-weight: 300;
            letter-spacing: 0.02em;
        '>Enterprise Agentic Intelligence Platform</p>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email    = st.text_input("Corporate Email", placeholder="you@karansystem.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit   = st.form_submit_button("Authenticate →")

        if submit:
            record = MOCK_USERS.get(email.strip())
            if record and record["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["user_data"] = record
                st.session_state["messages"]  = []
                st.rerun()
            else:
                st.error("Authentication failed — invalid credentials.")

        # Security badge
        st.markdown("""
        <div style="
            text-align: center;
            margin-top: 24px;
            color: #4a5568;
            font-size: 0.75rem;
            font-weight: 400;
            letter-spacing: 0.04em;
        ">
            <span style="color: #06d6a0;">●</span>&nbsp; End-to-end encrypted &nbsp;·&nbsp; SOC 2 Compliant &nbsp;·&nbsp; RBAC Enforced
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# ===============================================================================
# 2. MAIN INTERFACE — Command Center
# ===============================================================================
user    = st.session_state["user_data"]
role    = user["role"]
access  = ROLE_ACCESS.get(role, [])

# -- Sidebar — Control Deck ---------------------------------------------------
with st.sidebar:
    # Brand mark
    st.markdown("""
    <div style="
        display: flex; align-items: center; gap: 12px;
        margin-bottom: 24px; padding-bottom: 20px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    ">
        <div style="
            width: 36px; height: 36px; border-radius: 10px;
            background: linear-gradient(135deg, #06d6a0, #3b82f6);
            display: flex; align-items: center; justify-content: center;
            font-size: 1rem; box-shadow: 0 0 20px rgba(6,214,160,0.2);
        ">◆</div>
        <div>
            <div style="color: #f0f4f8; font-size: 0.85rem; font-weight: 700; letter-spacing: 0.02em;">KARAN SYSTEMS</div>
            <div style="color: #4a5568; font-size: 0.7rem; font-weight: 400; letter-spacing: 0.06em;">AGENTIC RAG v2.0</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # User identity card
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 16px;
    ">
        <div style="color: #7b8ba3; font-size: 0.7rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">Identity</div>
        <div style="color: #f0f4f8; font-size: 0.95rem; font-weight: 600; margin-bottom: 4px;">{user['name']}</div>
        <div style="color: #7b8ba3; font-size: 0.8rem;">{user.get('user_id', 'N/A')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Role & access card
    access_tags = " ".join([
        f'<span style="background:rgba(139,92,246,0.1); color:#8b5cf6; border:1px solid rgba(139,92,246,0.2); border-radius:6px; padding:3px 8px; font-size:0.7rem; font-weight:500; display:inline-block; margin:2px;">{a}</span>'
        for a in access
    ])
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 16px;
    ">
        <div style="color: #7b8ba3; font-size: 0.7rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">Security Context</div>
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
            <span style="color: #06d6a0; font-size: 0.6rem;">●</span>
            <span style="color: #f0f4f8; font-size: 0.85rem; font-weight: 600; text-transform: capitalize;">{role.replace('_', ' ')}</span>
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 4px;">
            {access_tags}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # System status
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 20px;
    ">
        <div style="color: #7b8ba3; font-size: 0.7rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px;">System Status</div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="color: #7b8ba3; font-size: 0.8rem;">RAG Pipeline</span>
                <span style="color: #06d6a0; font-size: 0.75rem; font-weight: 500;">● Active</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="color: #7b8ba3; font-size: 0.8rem;">Vector Store</span>
                <span style="color: #06d6a0; font-size: 0.75rem; font-weight: 500;">● Connected</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="color: #7b8ba3; font-size: 0.8rem;">Guardrails</span>
                <span style="color: #06d6a0; font-size: 0.75rem; font-weight: 500;">● Enforced</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⏻  Sign Out"):
        for k in ["logged_in", "user_data", "messages"]:
            st.session_state[k] = None if k == "user_data" else (
                False if k == "logged_in" else []
            )
        st.rerun()



# -- Page header ---------------------------------------------------------------
st.markdown(f"""
<div style="margin-bottom: 8px;">
    <h1 style="margin-bottom: 4px;">◆ {COMPANY}</h1>
    <p style='
        color: #7b8ba3;
        font-size: 0.95rem;
        font-weight: 300;
        margin: 0;
    '>Welcome back, <strong style="color: #f0f4f8; font-weight: 600;">{user['name']}</strong>
    <span style="margin: 0 8px; color: #2d3748;">|</span>
    <span style="
        background: rgba(6, 214, 160, 0.08);
        color: #06d6a0;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: capitalize;
        border: 1px solid rgba(6, 214, 160, 0.15);
    ">{role.replace('_', ' ')}</span></p>
</div>
""", unsafe_allow_html=True)

# Divider
st.markdown("""
<div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent); margin: 8px 0 20px 0;"></div>
""", unsafe_allow_html=True)

# -- Load agent (cached per session) ------------------------------------------
@st.cache_resource
def load_agent():
    try:
        return KaranAgenticRAG()
    except Exception as e:
        st.error(f"Initialisation error: {e}")
        st.stop()

agent = load_agent()

# -- Initialise chat history ---------------------------------------------------
if not st.session_state["messages"]:
    st.session_state["messages"] = [
        {
            "role":    "assistant",
            "content": f"Hello {user['name']}! I'm your enterprise AI assistant, powered by agentic RAG. "
                       f"Ask me anything about Karan Systems policies, "
                       f"incidents, or IT/HR processes.",
        }
    ]

# -- Render existing chat ------------------------------------------------------
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -- Query input ---------------------------------------------------------------
if prompt := st.chat_input("Ask about policies, incidents, or IT/HR processes..."):
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build assistant response
    with st.chat_message("assistant"):
        with st.spinner("Reasoning through your knowledge base..."):
            # Pass prior history (all messages except the last user turn)
            chat_history = st.session_state["messages"][:-1]
            response = agent.query(
                user_query=prompt,
                chat_history=chat_history,
                role=role,
            )
        st.markdown(response)

    st.session_state["messages"].append({"role": "assistant", "content": response})
