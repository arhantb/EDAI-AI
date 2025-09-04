import streamlit as st
from pathlib import Path
import sys

# Ensure project root (parent of this file's directory) is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.engine import PipelineEngine


st.set_page_config(page_title="Requirement-AI", layout="wide")
st.title("Requirement-AI: Automated Requirements Authoring")

with st.sidebar:
    st.header("Settings")
    input_dir = st.text_input("Input directory", value="data/docs")
    out_dir = st.text_input("Output directory", value="out")
    config_path = st.text_input("Config path", value="config/config.yaml")
    query = st.text_area("High-level query", value="Project requirements for current initiative")

if st.button("Run Pipeline"):
    engine = PipelineEngine(config_path)
    result = engine.run(input_dir, out_dir, query)
    st.success("Done")
    st.json(result)

out = Path(out_dir)
docx_path = out / "requirements.docx"
excel_path = out / "requirements.xlsx"
stories_path = out / "user_stories.txt"

if docx_path.exists():
    st.download_button("Download DOCX", data=docx_path.read_bytes(), file_name=docx_path.name)
if excel_path.exists():
    st.download_button("Download Excel", data=excel_path.read_bytes(), file_name=excel_path.name)
if stories_path.exists():
    st.download_button("Download User Stories", data=stories_path.read_bytes(), file_name=stories_path.name)


