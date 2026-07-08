import json

import pandas as pd
import streamlit as st

from extractor import extract_blood_work
from report_template import (
    DEFAULT_FORM_VALUES,
    DEFAULT_PASTE_REPORT,
    LAB_SECTIONS,
    build_report_text,
)


def load_sample_form_values() -> None:
    for field, value in DEFAULT_FORM_VALUES.items():
        st.session_state[field] = value


def load_default_paste_report() -> None:
    st.session_state.report_text = DEFAULT_PASTE_REPORT


if "form_initialized" not in st.session_state:
    load_sample_form_values()
    load_default_paste_report()
    st.session_state.form_initialized = True
elif "report_text" not in st.session_state:
    load_default_paste_report()


def get_template_report_text() -> str:
    test_values = {
        test_name: st.session_state.get(test_name, "")
        for section in LAB_SECTIONS
        for test_name, _ in section["tests"]
    }
    return build_report_text(
        patient_name=st.session_state.get("patient_name", ""),
        age=st.session_state.get("age", ""),
        gender=st.session_state.get("gender", ""),
        report_date=st.session_state.get("report_date", ""),
        physician=st.session_state.get("physician", ""),
        test_values=test_values,
    )


def analyze_report(report_text: str) -> None:
    if not report_text.strip():
        st.warning("Please enter or build a blood work report first.")
        return

    with st.spinner("Extracting blood work results..."):
        try:
            results = extract_blood_work(report_text)
            st.session_state.blood_work_results = results
        except ValueError as exc:
            st.session_state.pop("blood_work_results", None)
            st.error(str(exc))
        except Exception as exc:
            st.session_state.pop("blood_work_results", None)
            st.error(f"Failed to extract results: {exc}")


def render_results() -> None:
    if "blood_work_results" not in st.session_state:
        return

    results = st.session_state.blood_work_results
    rows = results.get("blood_work_results", [])

    st.subheader("Extracted results")
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No blood work results were found in the report.")

    with st.expander("Raw JSON"):
        st.code(json.dumps(results, indent=2), language="json")


st.set_page_config(page_title="Blood Work Analysis", page_icon="🩺", layout="wide")

st.title("Blood Work Analysis")
st.caption("Fill in a lab report template or paste your own report, then extract structured results.")

template_tab, paste_tab = st.tabs(["Fill lab report template", "Paste report text"])

with template_tab:
    st.subheader("Patient information")
    st.text_input("Patient name", key="patient_name", placeholder="John Smith")
    col1, col2, col3 = st.columns(3)
    col1.text_input("Age", key="age", placeholder="76")
    col2.text_input("Gender", key="gender", placeholder="Male")
    col3.text_input("Report date", key="report_date", placeholder="Dec 11, 2019")

    for section in LAB_SECTIONS:
        st.markdown(f"**{section['title']}**")
        cols = st.columns(2)
        for index, (test_name, placeholder) in enumerate(section["tests"]):
            with cols[index % 2]:
                st.text_input(test_name, key=test_name, placeholder=placeholder)

    st.text_input("Reviewing physician", key="physician", placeholder="Dr. Smith J")

    action_col1, action_col2, action_col3 = st.columns([1, 1, 2])
    with action_col1:
        if st.button("Reset to defaults", use_container_width=True):
            load_sample_form_values()
            st.rerun()
    with action_col2:
        analyze_template = st.button(
            "Analyze template report",
            type="primary",
            use_container_width=True,
        )

    generated_report = get_template_report_text()
    with st.expander("Preview generated report"):
        st.code(generated_report, language="text")

    if analyze_template:
        analyze_report(generated_report)

    render_results()

with paste_tab:
    paste_col1, paste_col2 = st.columns([1, 3])
    with paste_col1:
        if st.button("Reset to default report", use_container_width=True):
            load_default_paste_report()
            st.rerun()

    report_text = st.text_area(
        "Paste a blood work report",
        height=320,
        placeholder="Paste patient blood work text here...",
        key="report_text",
    )

    if st.button("Analyze pasted report", type="primary"):
        analyze_report(report_text)

    render_results()
