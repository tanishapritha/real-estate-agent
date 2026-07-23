# streamlit_app/pages/3_Knowledge_Base.py
"""Knowledge Base page.
Allows users to search the FAQ / policy knowledge base that the MCP `knowledge_server` backs.
"""

import streamlit as st
import requests

API_BASE = "http://localhost:8000"


def search_knowledge(query: str):
    try:
        resp = requests.get(f"{API_BASE}/knowledge/search", params={"q": query}, timeout=5)
        if resp.ok:
            return resp.json()
        else:
            st.warning(f"Knowledge endpoint returned {resp.status_code}")
    except Exception as e:
        st.error(f"Error contacting knowledge endpoint: {e}")
    return None


def placeholder_faqs():
    return [
        {"question": "How do I schedule a property visit?", "answer": "Use the calendar server's `available_slots` and `book_visit` tools."},
        {"question": "What financing options are available?", "answer": "We support mortgage, cash, and lease‑to‑own plans as described in the policies file."},
        {"question": "How can I update my contact information?", "answer": "Submit a request to the CRM server via the `update_stage` tool."},
    ]


def render() -> None:
    st.title("📚 Knowledge Base")
    st.markdown("Search FAQs and policy information used by the agents.")

    query = st.text_input("Enter search terms")
    if st.button("Search"):
        if not query.strip():
            st.info("Please enter a search query.")
            st.stop()
        results = search_knowledge(query)
        if not results:
            st.info("No live results – showing example FAQs.")
            results = placeholder_faqs()
        for item in results:
            with st.expander(item.get("question", "Untitled")):
                st.write(item.get("answer", ""))
