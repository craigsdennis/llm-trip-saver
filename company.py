import json

import streamlit as st

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    messages_from_dict,
    messages_to_dict,
)
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


@st.cache_resource
def get_chat():
    return ChatOpenAI(temperature=0.7)


chat = get_chat()

"""
# Company Trip

This will cause a company generated planned hallucination by industry.

"""

hallucination_prompt = "You are a creative serial entrepreneur. You have big ideas. You are a fan of technology. Describe your companies with popular buzzwords. When I ask you about your company it is okay to create fake but real sounding information."

def generate_company(industry):
    history = []
    prompts = [
        SystemMessagePromptTemplate.from_template(hallucination_prompt),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["industry"],
                template="I want you to pretend to have created a new company and name it something clever. It can be a made up word. It is in the {industry} industry. Tell me the name of your new company. Respond with the name only, no punctuation.",
            )
        ),
    ]
    chat_prompt = ChatPromptTemplate.from_messages(prompts)
    messages = chat_prompt.format_prompt(industry=industry).to_messages()
    ai = chat(messages)
    history.extend(messages)
    history.append(ai)
    company_name = ai.content
    company_interview = [
        "What is the elevator pitch for your company {company_name}?",
        "What is the mission statement for your company {company_name}?",
        "How does {company_name} make a profit?",
        "What communication methods does {company_name} use to communicate with it's customers?",
        "What products and/or services does {company_name} offer?",
        "What sort of customer events would {company_name} track in their CDP?",
    ]
    # Iterate over the question and re-prompt with hallucination
    for question in company_interview:
        prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["company_name"],
                template=question,
            )
        )
        # Copy
        prompts = list(history)
        prompts.append(prompt)
        chat_prompt = ChatPromptTemplate.from_messages(prompts)
        messages = chat_prompt.format_prompt(company_name=company_name).to_messages()
        current_question = messages[-1]
        ai = chat(messages)
        history.append(current_question)
        history.append(ai)
    st.session_state["history"] = history


industry = st.text_input("What industry would you like your fake company generated in?")
st.button("Generate", on_click=generate_company, args=(industry,))

st.markdown(f"> {hallucination_prompt}")

if "history" in st.session_state:
    for message in st.session_state["history"]:
        if isinstance(message, HumanMessage):
            st.markdown(f"#### {message.content}")
        elif isinstance(message, AIMessage):
            st.markdown(message.content)
    st.code(json.dumps(messages_to_dict(st.session_state["history"])))
