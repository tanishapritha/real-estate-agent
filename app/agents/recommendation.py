# app/agents/recommendation.py
"""Recommendation agent node.
Uses the LLM to generate property recommendations based on inventory matches.
Updates ``state.recommendation``.
"""

from typing import List, Dict, Any

from app.llm.gateway import call_model
from app.llm.guardrails import apply_guardrails
from app.agents.state import WorkflowState

def run(state: WorkflowState) -> WorkflowState:
    """Generate recommendations.
    Expects ``state.inventory_matches`` to be a list of property dicts.
    Returns updated state.
    """
    if not state.inventory_matches:
        raise ValueError("No inventory matches to recommend")
    # Build a simple prompt summarizing properties
    props_desc = "\n".join(
        f"- ID {p['id']}: {p.get('address', '')}, ${p.get('price', '')}" for p in state.inventory_matches
    )
    messages = apply_guardrails([
        {"role": "system", "content": "Given a list of property options, suggest the best one for the lead."},
        {"role": "user", "content": props_desc},
    ])
    llm_resp = call_model("recommendation", messages)
    try:
        recommendation_text = llm_resp["choices"][0]["message"]["content"]
    except Exception as e:
        raise ValueError(f"Unexpected LLM response: {e}")
    state.recommendation = {"text": recommendation_text, "options": state.inventory_matches}
    state.current_node = "recommendation"
    return state
