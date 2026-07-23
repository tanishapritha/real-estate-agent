# app/agents/graph.py
"""LangGraph wiring for the real‑estate agent workflow.
Defines the StateGraph that connects the individual agent nodes.
"""

from langgraph.graph import StateGraph

from .state import WorkflowState
from .qualification import run as qualification_node
from .inventory import run as inventory_node
from .recommendation import run as recommendation_node


def build_graph() -> StateGraph:
    """Construct and return the StateGraph.

    The graph order is:
        qualification → inventory → recommendation → END
    """
    graph = StateGraph(WorkflowState)

    # Register nodes
    graph.add_node("qualification", qualification_node)
    graph.add_node("inventory", inventory_node)
    graph.add_node("recommendation", recommendation_node)

    # Define flow
    graph.set_entry_point("qualification")
    graph.add_edge("qualification", "inventory")
    graph.add_edge("inventory", "recommendation")
    graph.add_edge("recommendation", "END")

    return graph

# Expose a ready‑to‑use graph instance for the app
workflow_graph = build_graph()
