from pydantic import BaseModel, Field

class WeatherParams(BaseModel):
    location: str = Field(..., description="City or coordinates")

class AnalyzeTextParams(BaseModel):
    text: str = Field(..., description="Text to analyze")

class DiagnosticsParams(BaseModel):
    system: str = Field(..., description="System name")
