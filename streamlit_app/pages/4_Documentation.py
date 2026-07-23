# streamlit_app/pages/4_Documentation.py
"""Documentation page.
Renders the repository markdown documentation files (architecture, agents, mcp, api).
"""

import streamlit as st
from pathlib import Path

DOCS_DIR = Path(__file__).parents[2] / "docs"


def list_md_files():
    if not DOCS_DIR.exists():
        return []
    return sorted(DOCS_DIR.glob("*.md"))


def read_md(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception as e:
        st.warning(f"Could not read {file_path.name}: {e}")
        return ""


def render() -> None:
    st.title("📖 Documentation")
    st.markdown("Browse the project documentation files.")

    md_files = list_md_files()
    if not md_files:
        st.info("No documentation files found in the `docs/` directory.")
        return

    doc_options = {f.name: f for f in md_files}
    selected = st.selectbox("Select document", list(doc_options.keys()))
    md_path = doc_options[selected]
    content = read_md(md_path)
    if content:
        st.markdown(content)
    else:
        st.info("Empty or unreadable document.")
