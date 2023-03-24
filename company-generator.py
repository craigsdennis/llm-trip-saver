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
    return ChatOpenAI(temperature=0.7, max_tokens=500)


chat = get_chat()

"""
# Company Trip

This will cause a company generated planned hallucination by industry.

"""

hallucination_prompt = "You are a creative serial entrepreneur. You have big ideas. You are a fan of technology. Describe your companies with popular buzzwords. When I ask you about your company it is okay to create fake but real sounding information."


def generate_company(industry):
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
        "What problems is {company_name} trying to solve by using its first party data? It is okay to create imaginary issues."
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
        prompts = list(company_history)
        prompts.append(prompt)
        chat_prompt = ChatPromptTemplate.from_messages(prompts)
        messages = chat_prompt.format_prompt(company_name=company_name).to_messages()
        current_question = messages[-1]
        ai = chat(messages)
        company_history.append(current_question)
        company_history.append(ai)
    st.session_state["company_history"] = company_history


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
    ai = chat(messages)
    code_history.extend([example_profile_prompt_message, ai])
    messages.append(ai)
    faker_prompt_message = HumanMessage(
        content="Based on that JSON example, create a Faker.js function that creates a profile. Return only JavaScript, no explanations"
    )
    messages.append(faker_prompt_message)
    ai = chat(messages)
    code_history.extend([faker_prompt_message, ai])
    st.session_state["code_history"] = code_history


industry = st.text_input("What industry would you like your fake company generated in?")
st.button("Generate", on_click=generate_company, args=(industry,))

st.markdown(f"> {hallucination_prompt}")

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
