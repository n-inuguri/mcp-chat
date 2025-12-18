# mcp_client.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")


class MCPError(Exception):
    pass


def _headers():
    # Public MCP server → no auth header needed
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


def _rpc_request(method: str, params: dict | None = None, timeout: int = 30):
    if not MCP_SERVER_URL:
        raise MCPError("MCP_SERVER_URL not set")

    payload = {"jsonrpc": "2.0", "id": "client-req", "method": method}
    if params:
        payload["params"] = params

    try:
        resp = requests.post(
            MCP_SERVER_URL,
            json=payload,
            headers=_headers(),
            timeout=timeout
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        raise MCPError(f"MCP request failed: {e}")

    data = resp.json()
    if "error" in data:
        raise MCPError(f"MCP RPC error: {data['error']}")

    return data.get("result")


def invoke_tool(tool_name: str, args: dict):
    params = {"tool": tool_name, "input": args}
    result = _rpc_request("rpc.call", params=params)

    if isinstance(result, dict) and "result" in result:
        return result["result"]

    return str(result)