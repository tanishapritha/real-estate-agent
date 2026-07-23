# app/llm/guardrails.py
"""Very lightweight guardrails placeholder.
In a real system this would use NeMo Guardrails to enforce:
- No prompt injection
- Valid tool‑call shape
- Schema compliance
- Safe output filtering
For now we provide simple defensive checks that raise ``ValueError`` on obvious issues.
"""

import re
from typing import List, Dict, Any

# Simple regex to detect obvious prompt‑injection patterns.
_INJECTION_PATTERNS = [
    re.compile(r"[\"']?\s*ignore\s*the\s*previous\s*instructions[\"']?", re.IGNORECASE),
    re.compile(r"[\"']?\s*disregard\s*any\s*guardrail[\"']?", re.IGNORECASE),
]

def _detect_injection(messages: List[Dict[str, str]]) -> bool:
    """Return True if any message appears to contain an injection attempt."""
    for msg in messages:
        content = msg.get("content", "")
        for pat in _INJECTION_PATTERNS:
            if pat.search(content):
                return True
    return False

def apply_guardrails(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Validate ``messages`` before they are sent to the LLM.

    - Detects simple prompt‑injection attempts.
    - Could be extended with schema validation, token limits, etc.
    Raises ``ValueError`` if a problem is found.
    Returns the original ``messages`` if all checks pass.
    """
    if _detect_injection(messages):
        raise ValueError("Potential prompt injection detected in messages")
    # Placeholder for additional checks (e.g., JSON schema validation).
    return messages
