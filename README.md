# 🧠 Demo MCP Tool Server

A minimal FastAPI implementation of the Model Context Protocol (MCP) for LLM tool integration.

## 🚀 Tools

- `get_weather`
- `analyze_text`
- `run_diagnostics`

## 🔧 Usage

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then visit:
- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
- MCP manifest: [http://localhost:8000/mcp/manifest.json](http://localhost:8000/mcp/manifest.json)
