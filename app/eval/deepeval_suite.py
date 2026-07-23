# app/eval/deepeval_suite.py
"""Placeholder DeepEval suite.
Add real evaluation logic later.
"""

def run_evaluation():
    """Run a simple sanity check for the workflow.
    Returns a dict with dummy metrics.
    """
    return {
        "hallucination": 0.0,
        "faithfulness": 1.0,
        "relevance": 1.0,
        "tool_correctness": 1.0,
        "routing_correctness": 1.0,
    }
