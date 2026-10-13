# 🤖 CodeBot AI – Coding Assistant

A premium AI-powered coding assistant built with **Streamlit** and **Groq**, using the `openai/gpt-oss-20b` model. Get instant, production-quality code for any programming language — with automatic improvement suggestions after every response.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?style=flat-square&logo=streamlit)
![Groq](https://img.shields.io/badge/Powered%20by-Groq-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- 💬 **Conversational chat interface** with full history
- ⚡ **Ultra-fast responses** via Groq's LPU inference
- 💡 **Auto improvement suggestions** — 3 clickable ideas after every code response
- 🎨 **Premium dark UI** — glassmorphism, gradients, JetBrains Mono font
- 📋 **Quick Prompts** sidebar for common coding tasks
- ⚙️ **Adjustable settings** — temperature, max token length
- 📊 **Session stats** — message count and token usage

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/codebot-ai.git
cd codebot-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Get a **free** Groq API key at 👉 [https://console.groq.com](https://console.groq.com)

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

### 5. Run the app

```bash
streamlit run main.py
```

Open your browser at **http://localhost:8501**

---

## 📁 Project Structure

```
codebot-ai/
├── main.py              # Streamlit application
├── requirements.txt     # Python dependencies
├── .env.example         # API key template (safe to commit)
├── .env                 # ← YOUR real key (gitignored, never commit!)
├── .gitignore           # Excludes secrets and venv
└── README.md
```

---

## 🔐 API Key Security

| File | Committed to Git? | Purpose |
|---|---|---|
| `.env` | ❌ **NO** (gitignored) | Your real API key |
| `.env.example` | ✅ Yes | Template for other users |
| `.gitignore` | ✅ Yes | Prevents secrets from being committed |

---

## 🌐 Deploying to Streamlit Cloud (Free Hosting)

1. Push this repo to GitHub (**without** `.env`)
2. Go to [https://share.streamlit.io](https://share.streamlit.io) and connect your repo
3. In the Streamlit Cloud dashboard → **Settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
4. Deploy — your app is live with a public URL!

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [Groq](https://groq.com) | Ultra-fast LLM inference API |
| `openai/gpt-oss-20b` | Language model |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Secure env variable loading |

---

## 📄 License

MIT License — free to use, modify, and distribute.
