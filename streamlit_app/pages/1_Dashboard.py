# streamlit_app/pages/1_Dashboard.py
"""Consolidated Dashboard page.
Includes flat header with health pill and 4 tabs: Overview, Workflows, Agents, Insights.
"""

import streamlit as st
import requests

from streamlit_app.components import overview, workflows, agents, insights

API_BASE = "http://localhost:8000"


def _check_health():
    try:
        resp = requests.get(f"{API_BASE}/health", timeout=3)
        if resp.ok:
            data = resp.json()
            return True, data.get("status", "ok")
        return False, f"HTTP {resp.status_code}"
    except Exception as e:
        return False, "offline"


def render() -> None:
    # ---- Flat Header Row ----
    is_ok, health_msg = _check_health()
    pill_color = "#10B981" if is_ok else "#EF4444"
    status_text = "All Systems Operational" if is_ok else f"System Issue: {health_msg}"

    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.markdown("<h2 style='margin:0; padding:0;'>🏠 RealEstate AI Sales OS</h2>", unsafe_allow_html=True)
    with header_col2:
        st.markdown(f"""
        <div style='text-align: right;'>
            <span style='background-color: {pill_color}22; color: {pill_color}; border: 1px solid {pill_color}; padding: 4px 12px; border-radius: 16px; font-size: 0.85em; font-weight: 600; display: inline-block;'>
                ● {status_text}
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

    # ---- 4 Tabs ----
    tab_names = ["Overview", "Workflows", "Agents", "Insights"]
    
    # Check if a tab was requested via session state (e.g. from Overview button)
    default_index = 0
    if "__tab__" in st.session_state and st.session_state["__tab__"] in tab_names:
        default_index = tab_names.index(st.session_state["__tab__"])

    tab_overview, tab_workflows, tab_agents, tab_insights = st.tabs(tab_names)

    with tab_overview:
        overview.render()

    with tab_workflows:
        workflows.render()

    with tab_agents:
        agents.render()

    with tab_insights:
        insights.render()
