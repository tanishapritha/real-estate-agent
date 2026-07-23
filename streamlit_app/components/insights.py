# streamlit_app/components/insights.py
"""Insights tab for the consolidated Dashboard.
Consolidates LangSmith viewer & Evaluation Center metrics, trace logs, and eval results.
"""
import streamlit as st
import requests

API_BASE = "http://localhost:8000"

def render():
    st.subheader("Performance & Evaluation Insights")

    # Top metrics row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='card'><div class='label'>Total Runs</div><div class='value'><b>1,248</b></div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card'><div class='label'>Success Rate</div><div class='value'><b>98.4%</b></div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='card'><div class='label'>Avg Cost / Lead</div><div class='value'><b>$0.042</b></div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='card'><div class='label'>User Satisfaction</div><div class='value'><b>4.9 / 5.0</b></div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Two sub-sections / sub-tabs or split view
    sub_tab1, sub_tab2 = st.tabs(["📊 Trace Logs (LangSmith)", "🧪 Evaluation Results"])

    with sub_tab1:
        st.markdown("##### Recent Execution Traces")
        col_search, col_filter = st.columns([3, 1])
        with col_search:
            st.text_input("Filter Traces by Tag / Name", placeholder="e.g. qualify_lead...")
        with col_filter:
            st.selectbox("Status Filter", ["All", "Success", "Error"])

        trace_data = [
            {"Trace ID": "tr-8910", "Agent / Run": "Qualification Workflow", "Latency": "1.2s", "Tokens": "480", "Status": "SUCCESS"},
            {"Trace ID": "tr-8911", "Agent / Run": "Inventory Search", "Latency": "0.4s", "Tokens": "120", "Status": "SUCCESS"},
            {"Trace ID": "tr-8912", "Agent / Run": "Recommendation Generation", "Latency": "2.8s", "Tokens": "1,050", "Status": "SUCCESS"},
            {"Trace ID": "tr-8913", "Agent / Run": "CRM Record Sync", "Latency": "0.3s", "Tokens": "95", "Status": "SUCCESS"},
        ]
        st.dataframe(trace_data, use_container_width=True)

        with st.expander("🔍 Expand Latency Spans & Span Tree (Sample: tr-8910)"):
            st.code("""
[Root] Qualification Workflow (1200ms)
  ├── [Tool] Get_Lead_Details (150ms)
  ├── [LLM] gpt-4o qualification prompt (850ms)
  └── [Tool] Save_Qual_Score (200ms)
            """, language="text")

    with sub_tab2:
        st.markdown("##### Benchmark Evaluation Center")
        test_suite = st.selectbox("Select Test Suite", ["Lead Qualification Accuracy v1", "Property Matching Precision", "CRM Schema Compliance"])
        
        col_eval1, col_eval2 = st.columns(2)
        with col_eval1:
            st.markdown("##### Pass Rates by Scenario")
            st.bar_chart({"Budget Extraction": 99, "Timeline Parsing": 96, "Location Preference": 98, "Constraint Handling": 94})
        with col_eval2:
            st.markdown("##### Test Benchmark Summary")
            st.markdown("""
            - **Selected Suite:** `{suite}`
            - **Total Test Cases:** 50
            - **Pass Rate:** 96.8%
            - **F1 Score:** 0.95
            - **Regression Delta:** +1.2% vs last run
            """.format(suite=test_suite))
