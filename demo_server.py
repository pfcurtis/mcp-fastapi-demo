# pip install "mcp[cli]" uvicorn
from mcp.server.fastmcp import FastMCP
import uvicorn

mcp = FastMCP("demo-tools")

@mcp.tool()
def get_weather(city: str = "Seattle", units: str = "metric") -> str:
    temp = "18" if units == "metric" else "65"
    return f"Weather in {city}: {temp}°, clear (dummy)."

@mcp.tool()
def analyze_text(text: str) -> str:
    wc, chars = len(text.split()), len(text)
    return f"words={wc}, chars={chars} (dummy)"

@mcp.tool()
def run_diagnostics(level: str = "quick") -> str:
    status = {"ok": True, "level": level, "checks": ["cpu: ok", "disk: ok", "net: ok"]}
    return f"diagnostics: {status}"

if __name__ == "__main__":
    # Expose an ASGI app that serves MCP over SSE at /sse (and /messages for posts)
    app = mcp.sse_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)

