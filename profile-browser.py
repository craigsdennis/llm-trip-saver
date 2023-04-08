from dotenv import load_dotenv

load_dotenv()

import json
import os

from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import pandas as pd
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


@st.cache_resource
def get_company_trip(company_name):
    return CompanyTrip.from_name(company_name)


company_trip = get_company_trip(company)

# You can append ?_limit=10&_page=2 https://github.com/typicode/json-server#paginate
profiles_url = f"https://llm-companies.cyclic.app/api/{company}/profiles"

browse_id = st.slider(f"Browse profiles for {company.title()}", max_value=50)

if browse_id > 0:
    response = requests.get(f"{profiles_url}/{browse_id}")
    profile = response.json()
    st.code(json.dumps(profile, indent=4))


with st.form("company-prompt"):
    company_prompt = st.text_area(f"This prompt is in context for {company}")
    submitted = st.form_submit_button("Ask")
    if submitted:
        answer = company_trip.ask(company_prompt)
        st.markdown(answer)

if company == "shadazzle":
    reviews_df = pd.read_json(os.path.join("trips", "data", "shadazzle-reviews.json"))

    # If you just return a string it will assume markdown
    "## First 5 reviews"
    # If you return a Pandas dataframe it will just render
    reviews_df[:5]

    @st.cache_resource
    def get_reviews_agent():
        # OpenAI is using the
        return create_pandas_dataframe_agent(
            OpenAI(model=os.environ["OPENAI_MODEL"], temperature=0),
            reviews_df,
            verbose=True,
        )

    agent = get_reviews_agent()

    with st.form("query_reviews"):
        reviews_query = st.text_area(
            "What would you like to know about this Reviews dataset?"
        )
        submitted = st.form_submit_button("Ask")
        if submitted:
            response = agent.run(reviews_query)
            st.markdown(response)
