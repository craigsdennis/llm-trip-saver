"""Temporary wrapper functions that assist LangChain issues

Google PaLM returns 0 and 1 for author and it confuses the current machinery.

"""

def convert_message_if_needed(message, MessageCls):
    if not isinstance(message, MessageCls):
        message = MessageCls(content=message.content)
    return message