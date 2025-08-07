from fastapi import FastAPI
from .schemas import WeatherParams, AnalyzeTextParams, DiagnosticsParams
from fastapi.responses import FileResponse
import json
import os

app = FastAPI(title="Demo MCP Tool Server")

BASE_DIR = os.path.dirname(__file__)

@app.get("/mcp/manifest.json", include_in_schema=False)
def get_manifest():
    with open(os.path.join(BASE_DIR, "manifest.json")) as f:
        return json.load(f)

@app.get("/logo.png", include_in_schema=False)
def logo():
    return FileResponse(os.path.join(BASE_DIR, "static/logo.png"))

@app.post("/tools/get_weather")
def get_weather(params: WeatherParams):
    return {
        "location": params.location,
        "forecast": "Sunny with 0% chance of rain. High: 25°C, Low: 15°C"
    }

@app.post("/tools/analyze_text")
def analyze_text(params: AnalyzeTextParams):
    return {
        "input": params.text,
        "analysis": {
            "sentiment": "neutral",
            "topic": "general"
        }
    }

@app.post("/tools/run_diagnostics")
def run_diagnostics(params: DiagnosticsParams):
    return {
        "system": params.system,
        "status": "Operational",
        "uptime": "42 days"
    }
