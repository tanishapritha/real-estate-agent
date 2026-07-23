# streamlit_app/pages/2_Lead_Intake.py
"""Lead Intake page for the Streamlit UI.
Provides a simple form to create a lead via the FastAPI `/leads/` endpoint.
"""

import streamlit as st
import requests

API_BASE = "http://localhost:8000"


def render() -> None:
    st.title("📝 Lead Intake")
    st.markdown("Enter lead information to start a new workflow.")

    with st.form(key="lead_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone (optional)")
        submit = st.form_submit_button("Create Lead")

    if submit:
        if not name or not email:
            st.error("Name and email are required.")
        else:
            payload = {"name": name, "email": email, "phone": phone or None}
            try:
                resp = requests.post(f"{API_BASE}/leads/", json=payload, timeout=5)
                if resp.ok:
                    data = resp.json()
                    st.success(f"Lead created with ID: {data.get('lead_id')}")
                else:
                    st.error(f"Failed to create lead: {resp.status_code} {resp.text}")
            except Exception as e:
                st.error(f"Error contacting API: {e}")
