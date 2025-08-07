from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_weather():
    response = client.post("/tools/get_weather", json={"location": "Berlin"})
    assert response.status_code == 200
    assert "forecast" in response.json()

def test_analyze_text():
    response = client.post("/tools/analyze_text", json={"text": "Hello world"})
    assert response.status_code == 200
    assert "analysis" in response.json()

def test_diagnostics():
    response = client.post("/tools/run_diagnostics", json={"system": "Mainframe"})
    assert response.status_code == 200
    assert "status" in response.json()
