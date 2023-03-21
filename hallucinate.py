import json
import requests
import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    messages_from_dict,
    messages_to_dict,
)


@st.cache_resource
def get_chat():
    return ChatOpenAI(temperature=0.7, max_tokens=500)


chat = get_chat()

"""
# Trip Saver

There are cases where you might want to force an AI hallucination and then save it
for replay to invite others in to the same context.
"""

"""
## System prompt

This is how you'd like the system to behave. You should be very specific, and make sure
that you tell it is okay to provide fake information. After you set this up, you can talk 
directly to it.
"""

if "system_locked" not in st.session_state:
    st.session_state["system_locked"] = False

system_prompter = st.text_area(
    "How should this assistant behave?",
    key="system_prompter",
    disabled=st.session_state["system_locked"],
)

"""
## Interact

Now you should interact with the assistant you just created.
"""

if "history" not in st.session_state:
    st.session_state["history"] = []
else:
    st.markdown("### History")


def remove_response_and_prompt(response_index):
    prompt_index = response_index - 1
    prompt = st.session_state["history"].pop(prompt_index)
    print(f"Removing prompt {prompt}")
    # Note since the list has shifted up we are using the same index
    ai = st.session_state["history"].pop(prompt_index)
    print(f"Removing ai result: {ai}")


for index, message in enumerate(st.session_state["history"]):
    if isinstance(message, HumanMessage):
        st.markdown(f"#### {message.content}")
    elif isinstance(message, AIMessage):
        st.markdown(message.content)
        st.button(
            "Remove this prompt",
            key=f"remove_{index}",
            on_click=remove_response_and_prompt,
            args=(index,),
        )


def submit_chat():
    messages = st.session_state["history"]
    if not messages:
        messages.append(SystemMessage(content=system_prompter))
    messages.append(HumanMessage(content=chat_prompter))
    ai_message = chat(messages)
    messages.append(ai_message)
    st.session_state["history"] = messages
    st.session_state["system_locked"] = True
    st.session_state.chat_prompter = ""


chat_prompter = st.text_area(
    "What would you like to ask your assistant?", key="chat_prompter"
)
st.button("Ask", on_click=submit_chat)

if st.session_state["history"]:
    number_of_tokens = chat.get_num_tokens_from_messages(st.session_state["history"])
    st.markdown(
        f"**Number of Tokens used in current conversation**: {number_of_tokens}"
    )


def import_json_url(url):
    response = requests.get(url)
    json = response.json()
    print(f"JSON was {json}")
    messages = messages_from_dict(json)
    st.session_state["history"] = messages
    st.session_state.system_prompter = messages[0].content
    st.session_state["system_locked"] = True


json_url = st.text_input("Import from JSON URL")
st.button("Import", on_click=import_json_url, args=(json_url,))

st.code(json.dumps(messages_to_dict(st.session_state["history"])))
