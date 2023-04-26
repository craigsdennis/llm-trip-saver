from dotenv import load_dotenv

load_dotenv()

import json
import os

from langchain.agents import create_pandas_dataframe_agent
from langchain.chains import APIChain
from langchain.chat_models import ChatOpenAI
import pandas as pd
import requests
import streamlit as st

from utils.trips import CompanyTrip


COMPANIES = ("shadazzle", "fitlyfe", "socimind")

"# Playground"

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


"## Using the `CompanyTrip` helper to load previous chat history"

with st.form("company-prompt"):
    company_prompt = st.text_area(f"This prompt is in context for {company}")
    submitted = st.form_submit_button("Ask")
    if submitted:
        answer = company_trip.ask(company_prompt)
        st.markdown(answer)

"""## Using the Profiles API documentation

This is using [LangChain's APIChain](https://python.langchain.com/en/latest/modules/chains/examples/api.html) to access the documentation for the API.
"""

@st.cache_data
def get_company_metadata(company):
    response = requests.get(f"https://llm-companies.cyclic.app/api/{company}/metadata")
    return response.json()


metadata = get_company_metadata(company)

with st.expander("API Docs"):
    st.code(metadata["docs"])


with st.form("profiles-api"):
    profiles_prompt = st.text_area(f"What would you like to ask the profiles API?")
    submitted = st.form_submit_button("Use API")
    if submitted:
        docs = metadata["docs"]
        llm = ChatOpenAI(model_name=os.environ["OPENAI_MODEL"], temperature=0)
        api_chain = APIChain.from_llm_and_api_docs(llm, docs, verbose=True)
        result = api_chain.run(profiles_prompt)
        st.write(result)

if company == "shadazzle":

    """## Experimenting with other data
    
This is using LangChain's [pandas DataFrame Agent](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/pandas.html)
    
"""

    reviews_df = pd.read_json(os.path.join("trips", "data", "shadazzle-reviews.json"))

    # If you just return a string it will assume markdown
    f"## First 5 of {len(reviews_df)} reviews"
    # If you return a Pandas dataframe it will just render
    reviews_df[:5]

    @st.cache_resource
    def get_reviews_agent():
        # OpenAI is using the
        return create_pandas_dataframe_agent(
            ChatOpenAI(model_name=os.environ["OPENAI_MODEL"], temperature=0),
            reviews_df,
            verbose=True,
        )

    reviews_agent = get_reviews_agent()

    with st.form("query_reviews"):
        reviews_query = st.text_area(
            "What would you like to know about this Reviews dataset?"
        )
        submitted = st.form_submit_button("Ask")
        if submitted:
            response = reviews_agent.run(reviews_query)
            st.write(response)
