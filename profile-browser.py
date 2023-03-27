import json

import requests
import streamlit as st

from utils import CompanyTrip

COMPANIES = ("shadazzle", "fitlyfe", "socimind")


company = st.selectbox(
    "Choose an existing Company Trip",
    options=COMPANIES,
    format_func=lambda x: x.title(),
    key="company",
)

profiles_url = f"https://llm-companies.cyclic.app/api/{company}/profiles"

browse_id = st.slider(f"Browse profiles for {company.title()}", max_value=50)

if browse_id > 0:
    response = requests.get(f"{profiles_url}/{browse_id}")
    profile = response.json()
    st.code(json.dumps(profile, indent=4))


with st.form("company-prompt"):
    company_prompt = st.text_area(f"This prompt is in context for {company}")
    submitted = st.form_submit_button("Ask")
    if (submitted):
        company_trip = CompanyTrip.from_name(company)
        answer = company_trip.ask(company_prompt)
        st.markdown(answer)

