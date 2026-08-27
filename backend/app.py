from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import os
import sys

# Import agent functions
from agents.lead_generator import collect_leads
from agents.enrichment_agent import enrich_all
from agents.lead_scorer import score_leads
from agents.engagement_agent import engage_leads
from agents.email_reply_collector import fetch_real_replies
from agents.sales_forecasting_agent import forecast_sales

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PipelineRequest(BaseModel):
    query: str

from fastapi import BackgroundTasks

# Global state to track pipeline progress
# In a production app, use Redis or a database.
pipeline_state = {
    "status": "idle",
    "message": "Ready",
    "steps_completed": 0
}

def execute_pipeline_task(query: str):
    global pipeline_state
    try:
        pipeline_state = {"status": "running", "message": "Starting lead generation...", "steps_completed": 0}
        
        # 1. Lead Generation
        pipeline_state["message"] = f"Searching for: {query}"
        count = collect_leads(query)
        if count == 0:
            raise Exception("No leads found for this query. Try a broader search term.")
        pipeline_state["steps_completed"] = 1
        
        # 2. Enrichment
        pipeline_state["message"] = "Enriching leads with contact info..."
        enrich_all()
        pipeline_state["steps_completed"] = 2
        
        # 3. Lead Scoring
        pipeline_state["message"] = "Scoring leads..."
        score_leads()
        pipeline_state["steps_completed"] = 3
        
        # 4. Engagement (Sending Emails)
        pipeline_state["message"] = "Sending engagement emails..."
        engage_leads()
        pipeline_state["steps_completed"] = 4
        
        # 5. Reply Collection
        pipeline_state["message"] = "Checking for replies..."
        fetch_real_replies()
        pipeline_state["steps_completed"] = 5
        
        # 6. Forecasting
        pipeline_state["message"] = "Generating sales forecast..."
        forecast_sales()
        pipeline_state["steps_completed"] = 6
        
        pipeline_state = {"status": "completed", "message": "Pipeline finished successfully", "steps_completed": 6}
        
    except Exception as e:
        print(f"Pipeline error: {e}")
        pipeline_state = {"status": "error", "message": str(e), "steps_completed": pipeline_state["steps_completed"]}

@app.post("/api/pipeline/run")
def run_pipeline(request: PipelineRequest, background_tasks: BackgroundTasks):
    if pipeline_state["status"] == "running":
         raise HTTPException(status_code=400, detail="Pipeline is already running")
         
    background_tasks.add_task(execute_pipeline_task, request.query)
    return {"status": "started", "message": "Pipeline execution started in background"}

@app.get("/api/pipeline/status")
def get_status():
    return pipeline_state

def _csv_records(path: str):
    """Read a CSV into JSON-safe records.

    The previous `df.where(pd.notnull(df), None)` looked like it replaced
    missing values, but on a float column pandas coerces the None straight back
    to NaN -- so NaN and inf survived. Starlette serialises responses with
    allow_nan=False, so /api/data/leads returned
    "ValueError: Out of range float values are not JSON compliant" (HTTP 500)
    whenever a scraped lead had a missing numeric field, which was almost
    always. That 500 is why the Leads, Dashboard and Analytics screens rendered
    empty even after the pipeline had finished successfully.

    Casting to object first stops the coercion, and inf is mapped to NaN before
    the replacement so it is nulled out too.
    """
    if not os.path.exists(path):
        return []
    try:
        df = pd.read_csv(path)
    except Exception as exc:  # noqa: BLE001 - a malformed CSV must not 500
        print(f"[!] Could not read {path}: {exc}")
        return []
    df = df.replace([np.inf, -np.inf], np.nan)
    return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")


@app.get("/api/data/forecast")
def get_forecast():
    return _csv_records("data/leads_forecasted.csv")


@app.get("/api/data/leads")
def get_leads():
    return _csv_records("data/leads_enriched.csv")


@app.get("/api/data/replies")
def get_replies():
    return _csv_records("data/replies.csv")


@app.get("/")
def read_root():
    return {"status": "AI Sales Agent Backend Running"}

if __name__ == "__main__":
    import uvicorn
    # Hugging Face Spaces uses port 7860 by default
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
