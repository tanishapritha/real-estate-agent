# app/mcp/client.py
"""Thin client for agents to invoke MCP server tools.
Usage:
    result = call_tool("crm", "create_lead", data={...})
The client looks up the server module via the registry and calls the named function.
"""

from typing import Any, Dict

from .registry import get_server_module

def call_tool(server_name: str, tool_name: str, **kwargs: Any) -> Dict[str, Any]:
    """Invoke a tool on the specified MCP server.

    Args:
        server_name: The registered name of the server (e.g., "crm").
        tool_name: The function name defined in the server module.
        **kwargs: Arguments forwarded to the tool function.
    Returns:
        The tool's return value (usually a dict).
    Raises:
        KeyError: If the server or tool is not found.
        AttributeError: If the tool function is missing.
    """
    module = get_server_module(server_name)
    func = getattr(module, tool_name)
    if not callable(func):
        raise AttributeError(f"{tool_name} on {server_name} is not callable")
    return func(**kwargs)
