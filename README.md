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

Example Docker build: docker --debug build  --push --platform linux/arm64,linux/amd64 --sbom=true --provenance=true -t pfcurtis/mcp-server-demo:0.1.3 

Then visit:
- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
- MCP manifest: [http://localhost:8000/mcp/manifest.json](http://localhost:8000/mcp/manifest.json)
