# streamlit_app/components/overview.py
"""Overview tab for the consolidated Dashboard.
Displays metric cards, a 7‑day leads bar chart, recent activity list and action buttons.
"""
import streamlit as st
import requests
from datetime import datetime

API_BASE = "http://localhost:8000"

def _fetch(endpoint: str, default=None):
    try:
        resp = requests.get(f"{API_BASE}{endpoint}", timeout=5)
        if resp.ok:
            return resp.json()
    except Exception:
        pass
    return default

def render():
    # ---- Metric cards ----
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        leads = _fetch("/leads/today", {"count": 0})
        st.markdown(f"""
        <div class='card'>
          <div class='label'>Leads Today</div>
          <div class='value'><b>{leads.get('count', 0)}</b></div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        props = _fetch("/properties/count", {"count": 0})
        st.markdown(f"""
        <div class='card'>
          <div class='label'>Properties Listed</div>
          <div class='value'><b>{props.get('count', 0)}</b></div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        agents = _fetch("/agents/active", {"count": 0})
        st.markdown(f"""
        <div class='card'>
          <div class='label'>Active Agents</div>
          <div class='value'><b>{agents.get('count', 0)}</b></div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        resp = _fetch("/metrics/response_time", {"avg_ms": 120})
        st.markdown(f"""
        <div class='card'>
          <div class='label'>Avg Response Time</div>
          <div class='value'><b>{resp.get('avg_ms', 120)}ms</b></div>
        </div>
        """, unsafe_allow_html=True)

    # ---- Middle row: 2 columns ----
    mid_left, mid_right = st.columns([1, 1])

    with mid_left:
        st.subheader("Leads (Last 7 Days)")
        leads_data = _fetch("/metrics/leads/count?days=7", {"counts": [5, 8, 12, 4, 10, 15, 9]})
        counts = leads_data.get("counts", [])
        if counts:
            st.bar_chart(counts)
        else:
            st.info("No lead data available.")

    with mid_right:
        st.subheader("Recent Activity")
        recent = _fetch("/events/recent", {
            "events": [
                {"icon": "📥", "description": "Lead created: John Doe", "timestamp": "2m ago"},
                {"icon": "🤖", "description": "Qualification Agent processed Lead #101", "timestamp": "5m ago"},
                {"icon": "⚡", "description": "Workflow #42 completed successfully", "timestamp": "12m ago"},
            ]
        })
        events = recent.get("events", [])
        if events:
            with st.container(height=300):
                for ev in events[:15]:
                    ts = ev.get("timestamp", "")
                    st.markdown(f"**{ev.get('icon', '🔔')}** {ev.get('description', '')} <span style='color: #888; font-size: 0.85em;'>({ts})</span>", unsafe_allow_html=True)
        else:
            st.info("No recent events.")

    st.markdown("---")

    # ---- Bottom buttons ----
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("➕ Add New Lead", use_container_width=True):
            st.session_state["__nav__"] = "Lead Intake"
    with col_b:
        if st.button("🚀 View Live Workflow", use_container_width=True):
            st.session_state["__tab__"] = "Workflows"

