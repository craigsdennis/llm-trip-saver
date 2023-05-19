from langchain.chat_models import ChatGooglePalm

from langchain.schema import (
    AIMessage,
    HumanMessage,
    AIMessage,
    SystemMessage
)

chat = ChatGooglePalm(temperature="0.7")

messages = [
    SystemMessage(content="You are an assistant"),
    HumanMessage(content="What is the capital of Arizona?"),
    #AIMessage(content="Phoenix"),
    #HumanMessage(content="What are the surrounding cities?")
]
response = chat(messages)
print(type(response))
print(response)