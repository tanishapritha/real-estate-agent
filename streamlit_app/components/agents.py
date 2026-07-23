# streamlit_app/components/agents.py
"""Agents tab for the consolidated Dashboard.
Displays a 3-column grid of specialist agent cards with status and prompt inspector.
"""
import streamlit as st
import requests

API_BASE = "http://localhost:8000"

def _fetch_agents():
    try:
        resp = requests.get(f"{API_BASE}/agents/", timeout=5)
        if resp.ok:
            return resp.json()
    except Exception:
        pass
    return [
        {"name": "Qualification Agent", "code": "qualification", "description": "Evaluates lead budget, timeline, and decision power.", "status": "active", "last_run": "2m ago"},
        {"name": "Inventory Agent", "code": "inventory", "description": "Searches property DB and matches specifications.", "status": "idle", "last_run": "15m ago"},
        {"name": "Recommendation Agent", "code": "recommendation", "description": "Generates tailored property recommendation cards.", "status": "idle", "last_run": "1h ago"},
        {"name": "Follow-Up Agent", "code": "followup", "description": "Handles automated follow-up messaging & nurture.", "status": "idle", "last_run": "3h ago"},
        {"name": "CRM Sync Agent", "code": "crm", "description": "Updates CRM records, syncs contact details and deal state.", "status": "active", "last_run": " Just now"},
    ]

def render():
    st.subheader("Specialist Agents Grid")
    agents = _fetch_agents()

    # 3-column layout
    cols = st.columns(3)
    for idx, ag in enumerate(agents):
        col = cols[idx % 3]
        with col:
            status_color = "#10B981" if ag.get("status") == "active" else "#6B7280"
            status_label = ag.get("status", "idle").upper()
            
            st.markdown(f"""
            <div class='card' style='margin-bottom: 1rem;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h4 style='margin:0;'>🤖 {ag.get("name")}</h4>
                    <span style='background-color: {status_color}22; color: {status_color}; border: 1px solid {status_color}; padding: 2px 8px; border-radius: 12px; font-size: 0.75em; font-weight: bold;'>
                        ● {status_label}
                    </span>
                </div>
                <p style='color: #AAA; font-size: 0.85em; margin-top: 8px;'>{ag.get("description")}</p>
                <div style='font-size: 0.8em; color: #888;'>Last run: {ag.get("last_run", "Never")}</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"🔍 Inspect Prompts ({ag.get('name')})"):
                st.markdown(f"**System Prompt ({ag.get('name')}):**")
                st.code(f"You are the {ag.get('name')} for RealEstate AI Sales OS. Analyze incoming lead data and execute relevant tools.", language="text")
                st.markdown("**Configured Tools:** `search_inventory`, `qualify_budget`, `update_crm`")
