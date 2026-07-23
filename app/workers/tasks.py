# app/workers/tasks.py
"""Celery tasks for the RealEstate agent system.
Currently handles the `LeadCreated` event by invoking the LangGraph workflow.
"""

import json
from typing import Dict

from app.events.schemas import LeadCreated
from app.agents.graph import workflow_graph
from app.agents.state import WorkflowState

# Import the Celery app defined in celery_app.py
from .celery_app import celery

@celery.task(name="process_lead_created")
def process_lead_created(event_json: str) -> str:
    """Celery task that processes a LeadCreated event.

    Parameters
    ----------
    event_json: str
        JSON string representation of a ``LeadCreated`` event.

    Returns
    -------
    str
        JSON string of the final ``WorkflowState`` after the graph run.
    """
    # Deserialize the incoming event
    event_dict: Dict = json.loads(event_json)
    lead_event = LeadCreated(**event_dict)

    # Initialise workflow state with the lead identifier
    state = WorkflowState(lead_id=lead_event.lead_id, current_node=None)

    # Run the StateGraph synchronously (in‑process) for this demo
    # ``invoke`` returns the final state after all nodes have executed
    final_state = workflow_graph.invoke(state)

    # Return the final state as JSON for visibility/debugging
    return final_state.json()
