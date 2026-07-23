# app/llm/gateway.py
"""Thin wrapper around LiteLLM to call LLM providers.
Provides a single function ``call_model`` that selects the provider based on the
role of the request (qualification, recommendation, summary, etc.).
Configuration is driven by environment variables defined in ``.env.example``.
"""

import os
from typing import List, Dict, Any

import litellm

# Map logical roles to Litellm model identifiers. Adjust as needed.
_ROLE_MODEL_MAP = {
    "qualification": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    "recommendation": os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20240620"),
    "summary": os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
}

def _prepare_messages(role: str, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Validate and return the message list for LiteLLM.
    ``messages`` should follow the OpenAI‑compatible schema:
    ``[{"role": "system|user|assistant", "content": "..."}, ...]``.
    """
    if not isinstance(messages, list) or not all(isinstance(m, dict) for m in messages):
        raise ValueError("messages must be a list of dicts with 'role' and 'content'")
    return messages

def call_model(role: str, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
    """Call the appropriate LLM for the given *role*.

    Args:
        role: Logical name of the operation (e.g. ``qualification``).
        messages: List of message dicts in OpenAI chat format.
        **kwargs: Additional LiteLLM parameters (temperature, max_tokens, …).

    Returns:
        The full response payload from LiteLLM (including ``choices``).
    """
    model_name = _ROLE_MODEL_MAP.get(role)
    if model_name is None:
        raise ValueError(f"Unsupported role '{role}'. Available: {list(_ROLE_MODEL_MAP)}")

    safe_messages = _prepare_messages(role, messages)
    response = litellm.completion(
        model=model_name,
        messages=safe_messages,
        **kwargs,
    )
    return response
