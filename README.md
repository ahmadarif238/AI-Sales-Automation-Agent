# 🤖 SalesAI: Automated Sales Pipeline

An AI-powered "Agent of Agents" system that automates B2B lead generation, enrichment, scoring, outreach, and sales forecasting.

Built with **Vite + React** (Frontend), **FastAPI** (Backend), **DuckDuckGo Search**, **BeautifulSoup4**, and **LLaMA 3** (via Groq).

---

## 🏗️ Project Structure

- `frontend/`: Vite + React application (React 19, Tailwind CSS).
- `backend/`: FastAPI application with specialized AI agents.

## 🚀 Deployment Guide

### 1. Backend: Hugging Face Spaces

1. Create a new **Space** on Hugging Face.
2. Select **Docker** as the SDK.
3. Push the contents of the `backend/` directory to the Space repository (or sync from GitHub).
4. Hugging Face will automatically build and run the `Dockerfile` on port 7860.
5. Set the required **Secrets** in your Space settings (see `.env.example` in root or backend).

### 2. Frontend: Vercel

1. Import your project into **Vercel**.
2. Set the root directory to `frontend/`.
3. Add the following **Environment Variable**:
   - `VITE_API_URL`: The URL of your Hugging Face Space (e.g., `https://your-space-name.hf.space`).
4. Build and deploy.

---

## ⚙️ Local Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/AI-Sales-Automation-Agent.git
   cd AI-Sales-Automation-Agent
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Create .env and add GROQ_API_KEY, EMAIL_ADDRESS, EMAIL_PASSWORD
   python app.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 🧑‍💻 Built By
Arif Ahmad Khan
Machine Learning Engineer & AI Automation Builder
