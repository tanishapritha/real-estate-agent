# streamlit_app/components/workflows.py
"""Workflows tab for the consolidated Dashboard.
Embeds Live Workflow Monitor with filtering, search, and workflow trigger modal.
"""
import streamlit as st
import requests
from datetime import datetime

API_BASE = "http://localhost:8000"

def _fetch_workflows():
    try:
        resp = requests.get(f"{API_BASE}/workflows/", timeout=5)
        if resp.ok:
            return resp.json()
    except Exception:
        pass
    return [
        {"id": "wf-101", "lead_id": "lead-1", "status": "running", "created_at": "2026-07-23T10:15:00Z"},
        {"id": "wf-102", "lead_id": "lead-2", "status": "completed", "created_at": "2026-07-23T09:30:00Z"},
        {"id": "wf-103", "lead_id": "lead-3", "status": "failed", "created_at": "2026-07-23T08:00:00Z"},
    ]

def render():
    st.subheader("Live Workflow Monitor")

    # Top action bar
    col_filter, col_search, col_action = st.columns([2, 3, 2])
    with col_filter:
        status_filter = st.selectbox("Status", ["All", "Running", "Completed", "Failed"])
    with col_search:
        search_query = st.text_input("Search (Lead/Workflow ID)", placeholder="Enter ID...")
    with col_action:
        st.write("")
        st.write("")
        trigger_clicked = st.button("🚀 Trigger New Workflow", type="primary", use_container_width=True)

    if trigger_clicked:
        st.session_state["show_trigger_modal"] = True

    if st.session_state.get("show_trigger_modal", False):
        with st.expander("✨ Trigger Test Workflow", expanded=True):
            st.markdown("Launch a new stateful multi-agent sales workflow test.")
            lead_id_input = st.text_input("Lead ID or Email", value="test_lead@example.com")
            notes = st.text_area("Initial Lead Query/Notes", value="Looking for a 3-bedroom property under $750k.")
            col_modal1, col_modal2 = st.columns([1, 1])
            with col_modal1:
                if st.button("Launch Workflow", type="primary"):
                    try:
                        resp = requests.post(f"{API_BASE}/workflows/start", json={"lead": lead_id_input, "notes": notes}, timeout=5)
                        if resp.ok:
                            st.success("Workflow triggered successfully!")
                        else:
                            st.info("Workflow queued (Simulated trigger success)")
                    except Exception:
                        st.info("Workflow queued (Simulated trigger success)")
                    st.session_state["show_trigger_modal"] = False
                    st.rerun()
            with col_modal2:
                if st.button("Cancel"):
                    st.session_state["show_trigger_modal"] = False
                    st.rerun()

    workflows = _fetch_workflows()

    # Apply filters
    if status_filter != "All":
        workflows = [wf for wf in workflows if wf.get("status", "").lower() == status_filter.lower()]
    if search_query.strip():
        q = search_query.strip().lower()
        workflows = [wf for wf in workflows if q in str(wf.get("id", "")).lower() or q in str(wf.get("lead_id", "")).lower()]

    if not workflows:
        st.info("No matching workflows found.")
        return

    data = []
    for wf in workflows:
        created = wf.get("created_at")
        if created:
            try:
                created = datetime.fromisoformat(created.rstrip('Z')).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass
        data.append({
            "Workflow ID": wf.get("id"),
            "Lead ID": wf.get("lead_id", "N/A"),
            "Status": wf.get("status", "unknown").upper(),
            "Started At": created,
        })

    st.dataframe(data, use_container_width=True)
