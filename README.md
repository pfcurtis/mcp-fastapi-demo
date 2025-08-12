# Demo MCP Server (SSE) + Client

This repo contains a **Model Context Protocol (MCP)** demo with:

- a minimal **MCP server** exposing **three dummy tools**  
  - `get_weather(city="Seattle", units="metric")`  
  - `analyze_text(text: str)`  
  - `run_diagnostics(level="quick")`
- a minimal **command-line client** that connects over **SSE** and calls any tool.

It’s built on the **official MCP Python SDK** and uses the **SSE transport** for maximum compatibility with other MCP clients.

---

## Prerequisites

- Python 3.9+
- (Recommended) A virtual environment

```bash
python -m venv env
source env/bin/activate           # Windows: env\Scripts\activate
```

## Install

```bash
pip install "mcp[cli]" uvicorn
```

> `mcp[cli]` installs the official SDK and client helpers. `uvicorn` runs the SSE server.

---

## Files

- `demo_server.py` — SSE MCP server exposing the 3 tools
- `demo_client.py` — CLI client that connects to the server over SSE and calls a tool

---

## Run the Server (SSE)

```bash
python demo_server.py
```

By default this hosts an SSE MCP endpoint at:

- **SSE stream:** `http://127.0.0.1:8000/sse`  
- **Message POST channel:** `http://127.0.0.1:8000/messages`

(These are provided by the SDK’s `mcp.sse_app()` helper and served by Uvicorn.)

---

## Use the Client

Open a second terminal (leave the server running) and call any tool.

### List tools + call `run_diagnostics`

```bash
python demo_client.py \
  --url http://127.0.0.1:8000/sse \
  --tool run_diagnostics \
  --data '{"level":"full"}'
```

**Expected output (example):**
```
Available tools: ['get_weather', 'analyze_text', 'run_diagnostics']

Result from run_diagnostics:
diagnostics: {'ok': True, 'level': 'full', 'checks': ['cpu: ok', 'disk: ok', 'net: ok']}
```

### Call `get_weather`

```bash
python demo_client.py \
  --url http://127.0.0.1:8000/sse \
  --tool get_weather \
  --data '{"city":"Paris","units":"imperial"}'
```

### Call `analyze_text`

```bash
python demo_client.py \
  --url http://127.0.0.1:8000/sse \
  --tool analyze_text \
  --data '{"text":"Hello there, general Kenobi."}'
```

---

## Server Code (for reference)

```python
# demo_server.py
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
    app = mcp.sse_app()                # exposes /sse and /messages
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Client Code (for reference)

```python
# demo_client.py
import asyncio
import argparse
import json
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    ap = argparse.ArgumentParser(description="Network MCP client (SSE)")
    ap.add_argument("--url", default="http://127.0.0.1:8000/sse",
                    help="SSE URL (default: http://127.0.0.1:8000/sse)")
    ap.add_argument("--tool", default="run_diagnostics", help="Tool to call")
    ap.add_argument("--data", default="{}", help='JSON payload, e.g. {"level":"full"}')
    args = ap.parse_args()

    payload = json.loads(args.data)

    async with sse_client(args.url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = [t.name for t in (await session.list_tools()).tools]
            print("Available tools:", tools)
            if args.tool not in tools:
                raise SystemExit(f"Tool '{args.tool}' not found. Choose: {tools}")

            result = await session.call_tool(args.tool, payload)
            print(f"\nResult from {args.tool}:")
            for c in result.content:
                print(getattr(c, "text", c))

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Troubleshooting

- **Client can’t connect / times out**
  - Ensure the server is running and listening on `http://127.0.0.1:8000`.
  - Confirm you’re using the SSE URL: `--url http://127.0.0.1:8000/sse`.

- **Tool not found**
  - The client prints `Available tools: [...]`. Use one of those names exactly.

- **Different port/host**
  - Start the server with a different port/host by editing `uvicorn.run(...)` in `demo_server.py`, then update the client `--url`.

- **Virtual environment issues**
  - Make sure both server and client are using the same venv (`which python` / `where python`).

---

## Why SSE?

SSE is widely supported across MCP clients and is easy to host behind common HTTP servers, making it a solid default for interoperability. If/when your target clients support **Streamable HTTP**, you can migrate this server by replacing `mcp.sse_app()` with a streamable-HTTP app and updating the client import to `streamablehttp_client`—the rest of the code (tool definitions and `ClientSession` flow) stays the same.

---

## License

MIT (or your choice—update as needed).
