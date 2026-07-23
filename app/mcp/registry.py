# app/mcp/registry.py
"""Central registry mapping MCP server names to their tool callables.
Each server module defines simple functions that agents can invoke.
The registry is a dict of {server_name: module} for easy lookup.
"""

from importlib import import_module
from typing import Dict, Any

# List of server modules – extend as new servers are added.
_SERVER_MODULES = {
    "crm": "app.mcp.servers.crm_server",
    "inventory": "app.mcp.servers.inventory_server",
    # future servers: calendar, messaging, knowledge, etc.
}

def get_server_module(server_name: str):
    """Return the imported module for the given server name.
    Raises KeyError if the server is not registered.
    """
    module_path = _SERVER_MODULES[server_name]
    return import_module(module_path)

def list_servers() -> Dict[str, str]:
    """Return a mapping of server name to module path for introspection."""
    return _SERVER_MODULES.copy()
