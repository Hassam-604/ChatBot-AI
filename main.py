import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load .env file if present (local development)
load_dotenv()

# ── Page configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="CodeBot AI – Coding Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS – premium dark glassmorphism UI ───────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0d0f14;
        color: #e2e8f0;
    }
    .stApp {
        background: linear-gradient(135deg, #0d0f14 0%, #111827 50%, #0d0f14 100%);
        min-height: 100vh;
    }

    /* ── Hide default Streamlit elements ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1.5rem 2rem 2rem 2rem !important; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
        border-right: 1px solid rgba(99,102,241,0.2);
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #a5b4fc;
    }

    /* ── Hero header ── */
    .hero-header {
        text-align: center;
        padding: 2rem 1rem 1rem;
        background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.10) 100%);
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 20px;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }
    .hero-header h1 {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818cf8, #a78bfa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 0.3rem 0;
    }
    .hero-header p {
        color: #94a3b8;
        font-size: 1rem;
        margin: 0;
    }

    /* ── Chat messages ── */
    .message-user {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 1rem;
    }
    .message-assistant {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 1rem;
    }
    .bubble-user {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: #fff;
        padding: 0.9rem 1.2rem;
        border-radius: 18px 18px 4px 18px;
        max-width: 75%;
        font-size: 0.95rem;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(99,102,241,0.35);
    }
    .bubble-assistant {
        background: rgba(30,41,59,0.85);
        border: 1px solid rgba(99,102,241,0.2);
        color: #e2e8f0;
        padding: 0.9rem 1.2rem;
        border-radius: 18px 18px 18px 4px;
        max-width: 85%;
        font-size: 0.95rem;
        line-height: 1.7;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    .avatar-user { background: linear-gradient(135deg, #4f46e5, #7c3aed); margin-left: 10px; }
    .avatar-bot  { background: linear-gradient(135deg, #0f766e, #0891b2); margin-right: 10px; }

    /* ── Improvement suggestions ── */
    .suggestions-box {
        background: rgba(15,23,42,0.8);
        border: 1px solid rgba(139,92,246,0.35);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-top: 0.8rem;
    }
    .suggestions-box h4 {
        color: #a78bfa;
        margin: 0 0 0.6rem 0;
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .suggestion-chip {
        display: inline-block;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(99,102,241,0.3);
        color: #a5b4fc;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        font-size: 0.82rem;
        margin: 0.25rem 0.25rem 0.25rem 0;
    }

    /* ── Input area ── */
    .stTextArea textarea {
        background: rgba(15,23,42,0.9) !important;
        border: 1px solid rgba(99,102,241,0.3) !important;
        border-radius: 14px !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 0.9rem 1rem !important;
        resize: vertical !important;
    }
    .stTextArea textarea:focus {
        border-color: rgba(99,102,241,0.7) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
    }
    .stTextArea textarea::placeholder { color: #4b5563 !important; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.8rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(99,102,241,0.35) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99,102,241,0.5) !important;
    }

    /* ── Select box ── */
    .stSelectbox > div > div {
        background: rgba(15,23,42,0.9) !important;
        border: 1px solid rgba(99,102,241,0.3) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }

    /* ── Code blocks ── */
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* ── Stats card ── */
    .stat-card {
        background: rgba(15,23,42,0.7);
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        text-align: center;
    }
    .stat-card .label { font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; }
    .stat-card .value { font-size: 1.4rem; font-weight: 700; color: #a5b4fc; }

    /* ── Divider ── */
    hr { border-color: rgba(99,102,241,0.15) !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0d0f14; }
    ::-webkit-scrollbar-thumb { background: #4f46e5; border-radius: 3px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Load API key ─────────────────────────────────────────────────────────────
# Priority: GROQ_API_KEY env var (set via .env) → legacy api_key.bt fallback

@st.cache_resource
def get_client():
    # 1. Try environment variable / .env file (recommended)
    key = os.getenv("GROQ_API_KEY", "").strip()

    # 2. Legacy fallback: read from .venv/api_key.bt (not committed to git)
    if not key:
        legacy_path = os.path.join(os.path.dirname(__file__), ".venv", "api_key.bt")
        try:
            with open(legacy_path, "r") as f:
                key = f.read().strip()
        except FileNotFoundError:
            pass

    if not key:
        st.error(
            "⚠️ **GROQ_API_KEY not found.**\n\n"
            "Create a `.env` file in the project root with:\n"
            "```\nGROQ_API_KEY=your_key_here\n```\n"
            "Get a free key at https://console.groq.com"
        )
        st.stop()

    return Groq(api_key=key)

client = get_client()
MODEL = "openai/gpt-oss-20b"

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = ""

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are **CodeBot**, an expert AI coding assistant.

Your primary job:
1. Generate clean, well-commented, production-quality code for any language or task.
2. Always wrap code in fenced code blocks with the correct language identifier.
3. After every response that contains code, add a section titled **"Improvement Ideas"** with exactly 3 concise bullet-point suggestions the user can explore next (e.g., add error handling, write tests, refactor, optimise, extend features).
4. Be precise, friendly, and educational. Explain your code briefly.
5. If the user picks an improvement idea, implement it fully.

Format your improvement section exactly like this (always at the end):

---
**Improvement Ideas**
- [Idea 1]
- [Idea 2]
- [Idea 3]
"""

# ── Helper: call Groq ─────────────────────────────────────────────────────────
def call_groq(user_message: str, temperature: float, max_tokens: int) -> tuple:
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in st.session_state.messages:
        history.append({"role": m["role"], "content": m["content"]})
    history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=MODEL,
        messages=history,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False,
    )
    text   = response.choices[0].message.content or ""
    tokens = response.usage.total_tokens if response.usage else 0
    return text, tokens


# ── Parse improvement ideas from response ─────────────────────────────────────
def extract_improvements(text: str) -> list:
    ideas = []
    in_section = False
    for line in text.splitlines():
        if "Improvement Ideas" in line:
            in_section = True
            continue
        if in_section:
            stripped = line.strip()
            if stripped.startswith("-") or stripped.startswith("*"):
                idea = stripped.lstrip("-*").strip()
                if idea:
                    ideas.append(idea)
            elif stripped == "" and ideas:
                break
    return ideas[:3]


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 CodeBot AI")
    st.markdown("*Your intelligent coding companion*")
    st.divider()

    st.markdown("### ⚙️ Settings")
    temperature = st.slider(
        "Creativity (Temperature)", 0.0, 1.0, 0.3, 0.05,
        help="Lower = more deterministic code. Higher = more creative."
    )
    max_tokens = st.select_slider(
        "Max Response Length",
        options=[512, 1024, 2048, 4096, 8192],
        value=2048,
    )

    st.divider()
    st.markdown("### 🌐 Model")
    st.markdown(f"`{MODEL}`")
    st.markdown("via **Groq** API")

    st.divider()
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="stat-card"><div class="label">Messages</div>'
            f'<div class="value">{len(st.session_state.messages)}</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        tokens_k = f"{st.session_state.total_tokens / 1000:.1f}k" \
            if st.session_state.total_tokens >= 1000 \
            else str(st.session_state.total_tokens)
        st.markdown(
            f'<div class="stat-card"><div class="label">Tokens</div>'
            f'<div class="value">{tokens_k}</div></div>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown("### 💡 Quick Prompts")
    quick_prompts = [
        "Write a REST API in Python using FastAPI",
        "Create a binary search algorithm in C++",
        "Build a React todo app with hooks",
        "SQL query to find duplicate rows",
        "Python web scraper with BeautifulSoup",
    ]
    for qp in quick_prompts:
        if st.button(qp, key=f"qp_{qp[:20]}", use_container_width=True):
            st.session_state.pending_prompt = qp
            st.rerun()

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_tokens = 0
        st.session_state.pending_prompt = ""
        st.rerun()


# ── Main content ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-header">
        <h1>🤖 CodeBot AI</h1>
        <p>Your intelligent coding assistant — describe what you need and get clean, production-ready code instantly.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Render chat history ───────────────────────────────────────────────────────
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(
            f'<div class="message-user">'
            f'<div class="bubble-user">{msg["content"]}</div>'
            f'<div class="avatar avatar-user">👤</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["content"])

        # Show improvement chips + apply buttons
        ideas = extract_improvements(msg["content"])
        if ideas:
            chips_html = "".join(
                f'<span class="suggestion-chip">✨ {idea}</span>'
                for idea in ideas
            )
            st.markdown(
                f'<div class="suggestions-box">'
                f'<h4>💡 Try these improvements</h4>'
                f'{chips_html}'
                f'</div>',
                unsafe_allow_html=True,
            )
            imp_cols = st.columns(len(ideas))
            for j, (col, idea) in enumerate(zip(imp_cols, ideas)):
                with col:
                    label = f"Apply: {idea[:32]}…" if len(idea) > 32 else f"Apply: {idea}"
                    if st.button(label, key=f"imp_{i}_{j}"):
                        st.session_state.pending_prompt = f"Please implement this improvement: {idea}"
                        st.rerun()

# ── Input area ────────────────────────────────────────────────────────────────
st.divider()
st.markdown("### ✍️ Ask CodeBot")

# Consume pending prompt
prefill = st.session_state.get("pending_prompt", "")
if prefill:
    st.session_state.pending_prompt = ""

user_input = st.text_area(
    label="Your coding question or request",
    value=prefill,
    placeholder="e.g. Write a Python function to merge two sorted lists…",
    height=120,
    label_visibility="collapsed",
    key="user_input_box",
)

send_col, hint_col = st.columns([1, 5])
with send_col:
    send_clicked = st.button("🚀 Generate Code", use_container_width=True)
with hint_col:
    st.markdown(
        "<small style='color:#4b5563;line-height:2.8'>Press **Generate Code** or pick a Quick Prompt from the sidebar.</small>",
        unsafe_allow_html=True,
    )

# ── Handle send ───────────────────────────────────────────────────────────────
if send_clicked and user_input.strip():
    prompt = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("🔧 Generating code…"):
        try:
            reply, tokens = call_groq(prompt, temperature, max_tokens)
            st.session_state.total_tokens += tokens
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"❌ API Error: {e}")

    st.rerun()
