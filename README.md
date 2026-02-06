---
title: AI Sales Automation Agent
emoji: 🚀
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
---

# 🤖 SalesAI: Next-Gen B2B Sales Automation

[![Vite](https://img.shields.io/badge/Frontend-Vite%20%2B%20React-646CFF?style=flat-square&logo=vite)](https://vitejs.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![LLaMA 3](https://img.shields.io/badge/AI-LLaMA%203%20(Groq)-orange?style=flat-square)](https://groq.com/)
[![Hugging Face](https://img.shields.io/badge/Deploy-Hugging%20Face%20Spaces-yellow?style=flat-square&logo=huggingface)](https://huggingface.co/spaces)

### 🚀 Standardizing B2B Prospecting with an "Agent of Agents" Architecture

Manual sales prospecting is slow, repetitive, and expensive. **SalesAI** is an intelligent, automated pipeline that handles the entire sales funnel—from finding raw leads to categorized sales forecasts—using a specialized swarm of 6 AI agents.

---

## 💡 The Problem & The Solution

**The Problem:** Sales teams spend 60% of their time on manual research, finding emails, and qualifying leads instead of actually selling.

**The Solution:** SalesAI automates the "grunt work." You provide a single search query, and the system orchestrates multiple sub-agents to deliver a qualified, scored, and engaged list of prospects.

---

## 🧠 Agent of Agents Architecture

Our system is composed of specialized sub-agents working in a deterministic pipeline:

| Agent | Responsibility |
| :--- | :--- |
| **Lead Generator** | Scours the web (DuckDuckGo) for companies matching your target audience. |
| **Enrichment Agent** | Scrapes websites to extract contact emails and business details. |
| **Lead Scorer** | Ranks leads based on data quality and ICP (Ideal Customer Profile) fit. |
| **Engagement Agent** | Crafts and sends personalized outreach emails via Gmail SMTP. |
| **Reply Monitor** | Tracks incoming responses using Gmail IMAP to detect interest. |
| **Forecaster** | Uses LLaMA 3 (via Groq) to categorize leads into **Hot**, **Warm**, or **Cold**. |

---

## 🛠️ Technical Stack

- **Frontend:** React 19, Vite, Tailwind CSS, Framer Motion (Animations), Recharts (Analytics).
- **Backend:** FastAPI, Python 3.11, Docker.
- **AI/LLM:** LLaMA 3 (Groq Cloud) for high-speed inference.
- **Data:** Pandas for pipeline state management and CSV-based persistence.

---

## 🚀 Deployment Guide

### 1. Backend: Hugging Face Spaces (Docker)
1. **Sync Repo:** Connect your GitHub to a new Docker-based HF Space.
2. **Set Secrets:** Add `GROQ_API_KEY`, `EMAIL_ADDRESS`, and `EMAIL_PASSWORD` to Space settings.
3. **Build:** The root `Dockerfile` ensures the FastAPI app builds and runs on port 7860.

### 2. Frontend: Vercel
1. **Import:** Connect your GitHub repo to Vercel.
2. **Root Dir:** Set to `frontend/`.
3. **Env Var:** Add `VITE_API_URL`. 
   - **Format:** `https://username-space-name.hf.space`
   - **Example:** `https://arifantarctic7-ai-sales-automation-agent.hf.space`
4. **Build:** Vercel will build your React app and it will talk to the HF backend.

## ⚙️ Local Development

1. **Clone & Setup:**
   ```bash
   git clone https://github.com/ahmadarif238/AI-Sales-Automation-Agent.git
   ```

2. **Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py # Server starts on http://localhost:7860
   ```

3. **Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev # Starts on http://localhost:5173
   ```

---

## 🧑‍💻 Built By
**Arif Ahmad Khan**  
*Machine Learning Engineer & AI Automation Specialist*  
[LinkedIn](https://linkedin.com/in/ahmadarif238) | [GitHub](https://github.com/ahmadarif238)
