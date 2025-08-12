# pip install "mcp[cli]"
import asyncio
import argparse
import json
from mcp import ClientSession
from mcp.client.sse import sse_client   # network transport (SSE)

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

