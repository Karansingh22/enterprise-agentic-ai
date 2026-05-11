import streamlit as st
from config import COMPANY, ROLE_ACCESS, MOCK_USERS
from agents.orchestrator import KaranAgenticRAG

# -- Page config --------------------------------------------------------------
st.set_page_config(
    page_title=f"{COMPANY} -- Agentic RAG",
    page_icon="[CORP]",
    layout="wide",
)

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
# 1. AUTHENTICATION
# ===============================================================================
if not st.session_state["logged_in"]:
    st.title(f"[CORP] {COMPANY} -- Secure Portal")
    st.markdown("Log in with your corporate credentials to access the RAG system.")

    with st.form("login_form"):
        email    = st.text_input("Corporate Email")
        password = st.text_input("Password", type="password")
        submit   = st.form_submit_button("Login")

        if submit:
            record = MOCK_USERS.get(email.strip())
            if record and record["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["user_data"] = record
                st.session_state["messages"]  = []
                st.rerun()
            else:
                st.error("[ERROR] Invalid corporate email or password.")
    st.stop()

# ===============================================================================
# 2. MAIN INTERFACE
# ===============================================================================
user    = st.session_state["user_data"]
role    = user["role"]

# -- Sidebar -------------------------------------------------------------------
with st.sidebar:
    st.header("🔐 Security Context")
    st.success(f"**{user['name']}**")
    st.code(f"Role: {role}")


    if st.button("Logout"):
        for k in ["logged_in", "user_data", "messages"]:
            st.session_state[k] = None if k == "user_data" else (
                False if k == "logged_in" else []
            )
        st.rerun()



# -- Page header ---------------------------------------------------------------
st.title(f"[CORP] {COMPANY} -- Enterprise Agentic RAG")
st.caption(
    f"Welcome back, **{user['name']}** · Role: `{role}`"
)

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
            "content": f"Hello {user['name']}! I'm your internal assistant. "
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
        with st.spinner("Retrieving from Pinecone and reasoning..."):
            # Pass prior history (all messages except the last user turn)
            chat_history = st.session_state["messages"][:-1]
            response = agent.query(
                user_query=prompt,
                chat_history=chat_history,
                role=role,
            )
        st.markdown(response)

    st.session_state["messages"].append({"role": "assistant", "content": response})
