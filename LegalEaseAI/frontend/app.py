import os

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="LegalEase AI", page_icon="⚖️")
st.title("LegalEase AI")
st.caption("Generate a polished legal document draft from a few inputs.")

with st.form("legal_document_form"):
    document_type = st.selectbox(
        "Document type",
        [
            "Services Agreement",
            "Employment Agreement",
            "Nondisclosure Agreement",
            "Partnership Agreement",
            "Independent Contractor Agreement",
        ],
    )
    parties = st.text_input("Parties involved", placeholder="Example: Acme Corp and Jane Doe")
    terms = st.text_area(
        "Key terms",
        value="Payment of $2,500 monthly, confidentiality obligations, termination for convenience, and dispute resolution in Delaware.",
        height=150,
    )
    dates = st.text_input("Dates and timing", placeholder="Example: Effective on 2026-10-01 and renewed annually")

    submitted = st.form_submit_button("Generate document")

if submitted:
    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "dates": dates,
    }

    try:
        with st.spinner("Preparing your document..."):
            response = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()

        st.success("Document generated successfully.")
        st.markdown(result["content"])
    except requests.exceptions.RequestException as exc:
        st.error(f"Unable to reach the backend at {BACKEND_URL}. Start the API server first.\n\n{exc}")