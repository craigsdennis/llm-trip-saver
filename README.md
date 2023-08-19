# LLM LGTM! 👍

This is a collection of [Streamlit](https://streamlit.io) applications that use [LangChain](https://langchain.com/) to create AI applications.

This is handy if you want to force a Large Language Model to create something and then play within the world it creates. Causing it to hallucinate is fun...and hallucinating is always better with friends.

We have created some example companies to explore and provide additional launching off points for you to build.

## Installation

Requires Python > 3.8 [Install](https://python.org)

You're going to need an [OpenAI API KEY](https://platform.openai.com/account/api-keys)

If you are at an event, we'll share the key with you.

Copy `.env.example` to `.env` and update with the key.

```bash
python -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the apps

### Quickstart

The [Playground](./playground.py) is a great place to start off point for learning Streamlit and LangChain

To run it locally: 

```bash
python -m streamlit run playground.py
```

This is also available as a [Python Notebook](profile-browser.ipynb)


### Run existing "trips" or create new ones

```bash
python -m streamlit run hallucinate.py
```

### Get the data

We have mocked the company data for you from previous Company Trips:

- [Shadazzle Profiles](https://llm-companies.cyclic.app/api/shadazzle/profiles?_limit=10)
- [Fitlyfe Profiles](https://llm-companies.cyclic.app/api/fitlyfe/profiles?_limit=10)
- [Socimind Profiles](https://llm-companies.cyclic.app/api/socimind/profiles?_limit=10)

## Prompt

Create a project that leverages the power of Segment CDP data and AI to enhance the customer experience for a "mock" business. Your project should use data from Twilio Segment CDP to generate insights and drive more personalized interactions with customers. Use your LLM to analyze customer behavior and preferences, and create a solution that automates and streamlines customer interactions, from initial outreach to post-purchase follow-up. Your solution could be a chatbot, voice assistant, or other conversational interface that uses natural language processing and machine learning to provide personalized recommendations, answer questions, and resolve issues.

We'd love you to share what you built, be sure to include:
- The business problem you're solving for
- The overview of your planned solution (could be a written outline or mocks, for example)
- A demo of whatever you've built so far.

We're not expecting a completely finished solution, but you should be able to clearly explain how your solution plans to use CDP data and an LLM to improve the customer experience.

### Examples

Here are a few examples to help get you in the right headspace:

- Create a chatbot that uses an LLM to generate personalized responses based on customer data stored in Twilio Segment. The chatbot should be able to handle complex queries and provide relevant information in a conversational tone.
- Build an email marketing campaign that uses an LLM to generate subject lines and email content based on customer data stored in Twilio Segment. The campaign should be able to target specific segments of customers and deliver personalized messages that resonate with them.
- Develop a voice assistant that uses an LLM to understand customer queries and respond with relevant information. The assistant should be able to access customer data stored in Twilio Segment and provide personalized recommendations based on their history and preferences.

Remember, the goal of this Hackathon is to inspire creativity and innovation in building better communications using customer data and communication channels from Twilio
