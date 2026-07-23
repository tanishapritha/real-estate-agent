# streamlit_app/Home.py
"""Entry point for the Streamlit UI.
Provides sidebar navigation across the consolidated pages:
- Dashboard (with Overview, Workflows, Agents, Insights tabs)
- Lead Intake
- Knowledge Base
- Documentation
"""

import importlib
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="RealEstate AI Sales OS", layout="wide")

# Load CSS
css_path = Path(__file__).parent / "static" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# Sidebar navigation
pages = {
    "Dashboard": "pages.1_Dashboard",
    "Lead Intake": "pages.2_Lead_Intake",
    "Knowledge Base": "pages.3_Knowledge_Base",
    "Documentation": "pages.4_Documentation",
}

# Handle programmatic navigation (e.g. from Dashboard buttons)
if "__nav__" in st.session_state and st.session_state["__nav__"] in pages:
    selected = st.session_state["__nav__"]
    del st.session_state["__nav__"]
else:
    selected = st.sidebar.selectbox("Navigate", list(pages.keys()))

module_name = pages[selected]
module = importlib.import_module(module_name)

if hasattr(module, "render"):
    module.render()
else:
    st.error(f"Page `{selected}` does not implement a `render()` function.")
