# app/llm/gateway.py
"""Thin wrapper around LiteLLM to call LLM providers (OpenAI, Anthropic, Gemini, Groq, etc.).
Provides a single function ``call_model`` that selects the provider based on the
role of the request (qualification, recommendation, summary, etc.).
"""

import os
from typing import List, Dict, Any
import litellm
from app.core.config import settings

def _get_default_model(role: str) -> str:
    # If GROQ_API_KEY is provided and set, default to Groq models
    if settings.GROQ_API_KEY and settings.GROQ_API_KEY != "mock-key":
        return os.getenv("GROQ_MODEL", "groq/llama-3.3-70b-versatile")
    
    role_defaults = {
        "qualification": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "recommendation": os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20240620"),
        "summary": os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
    }
    return role_defaults.get(role, "gpt-4o-mini")


def _prepare_messages(role: str, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    if not isinstance(messages, list) or not all(isinstance(m, dict) for m in messages):
        raise ValueError("messages must be a list of dicts with 'role' and 'content'")
    return messages


def call_model(role: str, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
    """Call the appropriate LLM for the given *role*."""
    model_name = _get_default_model(role)
    safe_messages = _prepare_messages(role, messages)
    
    # Pass Groq API key explicitly if using Groq
    if model_name.startswith("groq/") and settings.GROQ_API_KEY:
        kwargs["api_key"] = settings.GROQ_API_KEY

    response = litellm.completion(
        model=model_name,
        messages=safe_messages,
        **kwargs,
    )
    return response
