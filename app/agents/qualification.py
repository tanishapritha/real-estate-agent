# app/agents/qualification.py
"""Qualification agent node.
Calls the LLM to extract structured preferences from the lead's initial message.
Updates ``state.qualification`` and advances ``state.current_node``.
"""

from typing import Dict, Any

from app.llm.gateway import call_model
from app.llm.guardrails import apply_guardrails
from app.agents.state import WorkflowState

def run(state: WorkflowState) -> WorkflowState:
    """Execute qualification.
    Expects ``state.lead_id`` and an initial user message in ``state.messages``.
    Returns the updated state.
    """
    # Gather the latest user message
    user_msgs = [m for m in state.messages if m.get("sender") == "lead"]
    if not user_msgs:
        raise ValueError("No lead messages available for qualification")
    latest = user_msgs[-1]["content"]

    # Prepare LLM prompt (simple example)
    messages = apply_guardrails([
        {"role": "system", "content": "Extract the lead's preferences (budget, location, size) as JSON."},
        {"role": "user", "content": latest},
    ])

    llm_response = call_model("qualification", messages)
    # Assume the LLM returns a JSON in the first choice's message content
    try:
        extracted = llm_response["choices"][0]["message"]["content"]
    except Exception as e:
        raise ValueError(f"Unexpected LLM response format: {e}")
    # Store raw JSON string; downstream agents can parse as needed
    state.qualification = {"raw": extracted}
    state.current_node = "qualification"
    return state
