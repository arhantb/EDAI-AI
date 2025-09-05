import streamlit as st
from pathlib import Path
import sys
import os
from typing import Optional

try:
    import requests  # type: ignore
except Exception:
    requests = None

# Ensure project root (parent of this file's directory) is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.engine import PipelineEngine


st.set_page_config(page_title="Requirement-AI", layout="wide")
st.title("Requirement-AI: Automated Requirements Authoring")

with st.sidebar:
    st.header("Settings")
    mode = st.selectbox("Run mode", ["Local (in-process)", "API (upload to backend)"])
    query = st.text_area("High-level query", value="Project requirements for current initiative")
    out_dir = st.text_input("Output directory", value="out")
    config_path = st.text_input("Config path", value="config/config.yaml")
    if mode == "Local (in-process)":
        input_dir = st.text_input("Input directory", value="data/docs")
    else:
        api_url = st.text_input("Backend URL", value="http://127.0.0.1:8000")
        uploads = st.file_uploader("Upload documents", accept_multiple_files=True, type=["pdf","txt","doc","docx","png","jpg","jpeg"])

# Shared outline and helpers
OUTLINE_SECTIONS = [
    "INTRODUCTION",
    "PROJECT MANAGEMENT APPROACH",
    "PROJECT SCOPE",
    "MILESTONE LIST",
    "SCHEDULE BASELINE AND WORK BREAKDOWN STRUCTURE",
    "CHANGE MANAGEMENT PLAN",
    "COMMUNICATIONS MANAGEMENT PLAN",
    "COST MANAGEMENT PLAN",
    "PROCUREMENT MANAGEMENT PLAN",
    "PROJECT SCOPE MANAGEMENT PLAN",
    "SCHEDULE MANAGEMENT PLAN",
    "QUALITY MANAGEMENT PLAN",
    "RISK MANAGEMENT PLAN",
    "RISK REGISTER",
    "STAFFING MANAGEMENT PLAN",
    "RESOURCE CALENDAR",
    "COST BASELINE",
    "QUALITY BASELINE",
    "SPONSOR ACCEPTANCE",
]

def assign_section(text: str) -> str:
    # Fallback only; backend now annotates sections
    t = (text or "").upper()
    for sec in OUTLINE_SECTIONS:
        key = sec.split(" (")[0]
        if key in t:
            return sec
    return "OTHER"

def render_requirements_tab(result: dict, prefix: str) -> None:
    import pandas as pd
    import plotly.express as px  # type: ignore
    pr = result.get("prioritized", []) or []
    if not pr:
        st.info("No requirements extracted to display.")
        return
    df = pd.DataFrame(pr)
    if "section" not in df.columns:
        df["section"] = df["text"].map(assign_section)
    # Filters
    cols = st.columns([2, 2, 2])
    with cols[0]:
        sections = st.multiselect("Sections", OUTLINE_SECTIONS + ["OTHER"], default=OUTLINE_SECTIONS, key=f"{prefix}_sections")
    with cols[1]:
        moscow_filter = st.multiselect("MoSCoW", ["must","should","could","wont"], default=["must","should","could","wont"], key=f"{prefix}_moscow")
    with cols[2]:
        category_filter = st.multiselect("Category", sorted(df.get("category", pd.Series(["functional"]).repeat(len(df))).unique()), default=None, key=f"{prefix}_cat")
    f = df[df["section"].isin(sections) & df["moscow"].isin(moscow_filter)]
    if category_filter:
        f = f[f["category"].isin(category_filter)]
    # Visuals
    c1, c2 = st.columns(2)
    with c1:
        pie = px.pie(f, names="moscow", title="MoSCoW Distribution (Filtered)")
        st.plotly_chart(pie, width='stretch', key=f"{prefix}_pie_moscow")
    with c2:
        sec_bar = (f.groupby("section").size().reset_index(name="count"))
        bar = px.bar(sec_bar, x="section", y="count", title="Requirements by Section")
        bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(bar, width='stretch', key=f"{prefix}_bar_sections")
    # Sections summary from backend, if present
    if result.get("sections_summary"):
        st.subheader("Sections Summary")
        import pandas as pd
        ss = result.get("sections_summary")
        sdf = pd.DataFrame({"section": list(ss.keys()), "count": list(ss.values())})
        st.dataframe(sdf.sort_values("count", ascending=False), use_container_width=True)
    st.subheader("Requirements")
    st.dataframe(f[["text","section","category","moscow","priority_score"]].rename(columns={"text":"Requirement"}), use_container_width=True)

if st.button("Run Pipeline"):
    if mode == "Local (in-process)":
        engine = PipelineEngine(config_path)
        result = engine.run(input_dir, out_dir, query)
        st.success("Done")
        tab_overview, tab_requirements = st.tabs(["Overview","Requirements"])
        with tab_overview:
            st.subheader("Result Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Chunks", result.get("num_chunks", 0))
            col2.metric("Candidates", result.get("num_candidates", 0))
            col3.metric("Files", len(result.get("files", [])))

            st.subheader("Document Outline")
            for sec in OUTLINE_SECTIONS:
                st.checkbox(sec, value=True, key=f"outline_{sec}")

            # MoSCoW pie chart
            st.subheader("MoSCoW Prioritization")
        try:
            import pandas as pd
            import plotly.express as px  # type: ignore
            pr = result.get("prioritized", [])
            df = pd.DataFrame(pr)
            if not df.empty and "moscow" in df.columns:
                pie = px.pie(df, names="moscow", title="MoSCoW Distribution")
                st.plotly_chart(pie, width='stretch')
        except Exception as _:
            pass

            # Risk pie placeholder (depends on validation flags)
            st.subheader("Risk & Validation Overview")
        validation = result.get("validation", {}) or {}
        flags = validation.get("flags", []) or []
        risk_counts = {"conflicts": 0, "ambiguity": 0, "missing": 0}
        for f in flags:
            txt = str(f).lower()
            if "conflict" in txt:
                risk_counts["conflicts"] += 1
            if "ambigu" in txt:
                risk_counts["ambiguity"] += 1
        missing = validation.get("missing", []) or []
        risk_counts["missing"] = len(missing)
        try:
            import pandas as pd
            import plotly.express as px  # type: ignore
            rpdf = pd.DataFrame({"type": list(risk_counts.keys()), "count": list(risk_counts.values())})
            rpie = px.pie(rpdf, names="type", values="count", title="Risk Summary")
            st.plotly_chart(rpie, width='stretch')
        except Exception:
            pass

            # User stories
            st.subheader("User Stories")
            stories = result.get("user_stories", [])
            if stories:
                for s in stories:
                    st.markdown(f"- {s}")
            else:
                st.info("No user stories generated.")

            with st.expander("Raw Result JSON"):
                st.json(result)

        with tab_requirements:
            render_requirements_tab(result, prefix="local")
    else:
        if requests is None:
            st.error("'requests' is not installed. Please install it to use API mode: pip install requests")
        elif not api_url:
            st.error("Please provide Backend URL")
        elif not uploads:
            st.error("Please upload at least one document")
        else:
            try:
                files = [("files", (u.name, u.getvalue())) for u in uploads]
                data = {"query": query, "out_dir": out_dir, "config_path": config_path}
                resp = requests.post(api_url.rstrip("/") + "/upload-and-process", files=files, data=data, timeout=600)
                if resp.status_code != 200:
                    st.error(f"Backend error {resp.status_code}: {resp.text}")
                else:
                    payload = resp.json()
                    st.success("Done")
                    result = payload.get("result", {})
                    tab_overview, tab_requirements = st.tabs(["Overview","Requirements"])
                    with tab_overview:
                        st.subheader("Result Summary")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Chunks", result.get("num_chunks", 0))
                        col2.metric("Candidates", result.get("num_candidates", 0))
                        col3.metric("Files", len(result.get("files", [])))

                        # Outline
                        st.subheader("Document Outline")
                        for sec in OUTLINE_SECTIONS:
                            st.checkbox(sec, value=True, key=f"api_outline_{sec}")

                        # MoSCoW pie
                    try:
                        import pandas as pd
                        import plotly.express as px  # type: ignore
                        pr = result.get("prioritized", [])
                        df = pd.DataFrame(pr)
                        if not df.empty and "moscow" in df.columns:
                            pie = px.pie(df, names="moscow", title="MoSCoW Distribution")
                            st.plotly_chart(pie, use_container_width=True)
                    except Exception:
                        pass

                        # Risk
                    validation = result.get("validation", {}) or {}
                    flags = validation.get("flags", []) or []
                    risk_counts = {"conflicts": 0, "ambiguity": 0, "missing": 0}
                    for f in flags:
                        txt = str(f).lower()
                        if "conflict" in txt:
                            risk_counts["conflicts"] += 1
                        if "ambigu" in txt:
                            risk_counts["ambiguity"] += 1
                    missing = validation.get("missing", []) or []
                    risk_counts["missing"] = len(missing)
                    try:
                        import pandas as pd
                        import plotly.express as px  # type: ignore
                        rpdf = pd.DataFrame({"type": list(risk_counts.keys()), "count": list(risk_counts.values())})
                        rpie = px.pie(rpdf, names="type", values="count", title="Risk Summary")
                        st.plotly_chart(rpie, use_container_width=True)
                    except Exception:
                        pass

                        # Stories
                        st.subheader("User Stories")
                        stories = result.get("user_stories", [])
                        if stories:
                            for s in stories:
                                st.markdown(f"- {s}")
                        else:
                            st.info("No user stories generated.")

                        with st.expander("Raw Result JSON"):
                            st.json(result)

                    with tab_requirements:
                        render_requirements_tab(result, prefix="api")
                    artifacts = payload.get("artifacts", {})
                    out = Path(out_dir)
                    st.subheader("Artifacts")
                    docx_path = Path(artifacts.get("docx", out / "requirements.docx"))
                    excel_path = Path(artifacts.get("excel", out / "requirements.xlsx"))
                    stories_path = Path(artifacts.get("stories", out / "user_stories.txt"))

                    if docx_path.exists():
                        st.download_button("Download DOCX", data=docx_path.read_bytes(), file_name=docx_path.name, key="api_download_docx")
                    if excel_path.exists():
                        st.download_button("Download Excel", data=excel_path.read_bytes(), file_name=excel_path.name, key="api_download_excel")
                    if stories_path.exists():
                        st.download_button("Download User Stories", data=stories_path.read_bytes(), file_name=stories_path.name, key="api_download_stories")
            except Exception as e:
                st.error(str(e))

out = Path(out_dir)
docx_path = out / "requirements.docx"
excel_path = out / "requirements.xlsx"
stories_path = out / "user_stories.txt"

st.divider()
st.caption("Local artifact downloads (if present on this machine)")
if docx_path.exists():
    st.download_button("Download DOCX", data=docx_path.read_bytes(), file_name=docx_path.name, key="local_download_docx")
if excel_path.exists():
    st.download_button("Download Excel", data=excel_path.read_bytes(), file_name=excel_path.name, key="local_download_excel")
if stories_path.exists():
    st.download_button("Download User Stories", data=stories_path.read_bytes(), file_name=stories_path.name, key="local_download_stories")


