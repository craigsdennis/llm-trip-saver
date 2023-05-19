import os
import json

from dotenv import load_dotenv

load_dotenv()


import streamlit as st

from langchain import PromptTemplate
from langchain.chat_models import ChatGooglePalm
from langchain.schema import (
    AIMessage,
    HumanMessage,
    messages_to_dict,
)
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from utils.google_palm_tools import convert_message_if_needed


@st.cache_resource
def get_chat():
    return ChatGooglePalm(temperature=0.7)


chat = get_chat()

"""
# Company Trip

This will cause a company generated planned hallucination by industry.

"""

hallucination_prompt = "You are a creative serial entrepreneur. You have big ideas. You are a fan of technology. Describe your companies with popular buzzwords. When I ask you about your company it is okay to create fake but real sounding information."
generation_progress = st.progress(0, "Awaiting Input")


def generate_company(industry=None):
    if industry is None:
        industry = st.session_state["industry"]
    company_history = []
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
    ai = convert_message_if_needed(ai, AIMessage)
    company_history.extend(messages)
    company_history.append(ai)
    company_name = ai.content
    st.session_state["company_name"] = company_name
    company_interview = [
        "What is the elevator pitch for your company {company_name}?",
        "What is the mission statement for your company {company_name}?",
        "How does {company_name} make a profit?",
        "What communication methods does {company_name} use to communicate with it's customers?",
        "What products and/or services does {company_name} offer?",
        "What sort of customer events would {company_name} track in their CDP?",
        "What problems is {company_name} trying to solve by using its first party data? It is okay to create imaginary issues.",
    ]
    # Iterate over the question and re-prompt with hallucination
    for index, question in enumerate(company_interview):
        prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["company_name"],
                template=question,
            )
        )
        # Copy
        prompts = list(company_history)
        prompts.append(prompt)
        chat_prompt = ChatPromptTemplate.from_messages(prompts)
        messages = chat_prompt.format_prompt(company_name=company_name).to_messages()
        current_question = messages[-1]
        generation_progress.progress(
            index / len(company_interview), f"Prompting: {current_question.content}"
        )
        company_history.append(current_question)
        ai_message = chat(messages)
        ai_message = convert_message_if_needed(ai_message, AIMessage)
        company_history.append(ai_message)
    st.session_state["company_history"] = company_history
    return company_history


def generate_code():
    code_history = []
    # Use a copy of the existing messages
    messages = list(st.session_state["company_history"])
    # Generate CDP API response using prompt template
    example_profile_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            template="Create an example {company_name} CDP based user profile in JSON format. Include rollup traits like ltv and cac. It should look like the profiles that Segment returns from it's Profile API. Return only the JSON, no explanations.",
            input_variables=["company_name"],
        )
    )
    example_profile_prompt_message = example_profile_prompt.format(
        company_name=st.session_state["company_name"]
    )
    messages.append(example_profile_prompt_message)
    print(f"Human", example_profile_prompt)
    ai_message = chat(messages)
    ai_message = convert_message_if_needed(ai_message, AIMessage)
    code_history.extend([example_profile_prompt_message, ai_message])
    messages.append(ai_message)
    faker_prompt_message = HumanMessage(
        content="Based on that JSON example, create a Faker.js function that creates a profile. Return only JavaScript, no explanations"
    )
    messages.append(faker_prompt_message)
    ai_message = chat(messages)
    ai_message = convert_message_if_needed(ai_message, AIMessage)

    code_history.extend([faker_prompt_message, ai_message])
    st.session_state["code_history"] = code_history


with st.form("industry-form"):
    industry = st.text_input(
        "What industry would you like your fake company generated in?", key="industry"
    )
    submitted = st.form_submit_button("Generate", on_click=generate_company)
    st.markdown(f"> {hallucination_prompt}")
    if submitted:
        generation_progress.empty()

if "company_history" in st.session_state:
    for message in st.session_state["company_history"]:
        if isinstance(message, HumanMessage):
            st.markdown(f"#### {message.content}")
        elif isinstance(message, AIMessage):
            st.markdown(message.content)
    st.markdown(
        f"""
    ## Code Generation

    What could go wrong? 🙃

    """
    )
    st.button(
        "Generate code",
        on_click=generate_code,
    )

    if "code_history" in st.session_state:
        for message in st.session_state["code_history"]:
            if isinstance(message, HumanMessage):
                st.markdown(f"> {message.content}")
            elif isinstance(message, AIMessage):
                st.code(message.content)

    st.markdown("### The company exported as replayable JSON")
    st.code(json.dumps(messages_to_dict(st.session_state["company_history"]), indent=4))
