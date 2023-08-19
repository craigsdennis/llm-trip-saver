import json
import os

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage,
    AIMessage,
    messages_from_dict,
)
import streamlit as st


COMPANIES = ("shadazzle", "fitlyfe", "socimind")


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


with st.sidebar:

    def import_json(json_obj):
        messages = messages_from_dict(json_obj)
        st.session_state["messages"] = messages[1:]
        st.session_state["system_prompter"] = messages[0].content
        st.session_state["system_locked"] = True
        st.balloons()

    with st.form("Load Trip"):
        company = st.selectbox(
            "Choose an existing Company Trip",
            options=COMPANIES,
            format_func=lambda x: x.title(),
            key="company",
        )
        submitted = st.form_submit_button("🧳 Load")
        if submitted:
            full_filepath = os.path.join("trips", "companies", company + ".json")
            with open(full_filepath) as file:
                json_str = file.read()
                import_json(json.loads(json_str))

    if "system_locked" not in st.session_state:
        st.session_state["system_locked"] = False

    system_prompter = st.text_area(
        "How should this assistant behave?",
        key="system_prompter",
        disabled=st.session_state["system_locked"],
    )

    def reset():
        st.session_state["system_prompter"] = ""
        st.session_state["messages"] = []
        st.session_state["system_locked"] = False
        st.balloons()

    st.button("♻️ Reset", on_click=reset)


@st.cache_resource
def get_chat():
    return ChatOpenAI(model=os.environ["OPENAI_MODEL"], streaming=True)


if "messages" not in st.session_state:
    st.session_state["messages"] = [AIMessage(content="How can I help you?")]

for msg in st.session_state.messages:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    st.chat_message(role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        chat = get_chat()
        chat.callbacks = [stream_handler]
        system_message = SystemMessage(content=system_prompter)
        response = chat([system_message] + st.session_state.messages)
        st.session_state.messages.append(response)
        # Don't change system message after you got a response
        st.session_state["system_locked"] = True
