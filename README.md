# Trip Saver

This is a [Streamlit](https://streamlit.io) application that uses [Langchain](https://langchain.com/) to produce a ChatGPT interface. It allows you to import, export and modify previous conversations.

This is handy if you want to force GPT to create something and then play within the world it creates. Causing it to hallucinate is fun...and hallucinating is always better with friends.

## Installation

Requires Python > 3.8 [Install](https://python.org)

You're going to need an [OpenAI API Key](https://platform.openai.com/account/api-keys)

If you are at an event, we'll share the key with you.

Copy `.env.example` to `.env` and update with the key.

```bash
python -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the apps


### Run existing "trips" or create new ones

```bash
streamlit run hallucinate.py
```

### Browse profiles from existing companies

```bash
streamlit run profile-browser.py
```

This is also available as a [Python Notebook](profile-browser.ipynb)

### Get the data

We have mocked the company data for you:

- [Shadazzle Profiles](https://llm-companies.cyclic.app/api/shadazzle/profiles?_limit=10)
- [Fitlyfe Profiles](https://llm-companies.cyclic.app/api/fitlyfe/profiles?_limit=10)
- [Socimind Profiles](https://llm-companies.cyclic.app/api/socimind/profiles?_limit=10)

## Prompt

Create a project that leverages the power of Segment CDP data and AI to enhance the customer experience for a "mock" business. Your project should use data from Twilio Segment CDP to generate insights and drive more personalized interactions with customers. Use GPT-3 (or another LLM that you have access to) to analyze customer behavior and preferences, and create a solution that automates and streamlines customer interactions, from initial outreach to post-purchase follow-up. Your solution could be a chatbot, voice assistant, or other conversational interface that uses natural language processing and machine learning to provide personalized recommendations, answer questions, and resolve issues.

After 2 hours of hacking, you'll present:
- The business problem you're solving for
- The overview of your planned solution (could be a written outline or mocks, for example)
- A demo of whatever you've built so far.

We're not expecting a completely finished solution, but you should be able to clearly explain how your solution plans to use CDP data and an LLM to improve the customer experience.

### Examples

Here are a few examples to help get you in the right headspace:

- Create a chatbot that uses GPT to generate personalized responses based on customer data stored in Twilio Segment. The chatbot should be able to handle complex queries and provide relevant information in a conversational tone.
- Build an email marketing campaign that uses GPT to generate subject lines and email content based on customer data stored in Twilio Segment. The campaign should be able to target specific segments of customers and deliver personalized messages that resonate with them.
- Develop a voice assistant that uses GPT to understand customer queries and respond with relevant information. The assistant should be able to access customer data stored in Twilio Segment and provide personalized recommendations based on their history and preferences.

Remember, the goal of this Hackathon is to inspire creativity and innovation while highlighting the value of having all your customer data in one place like Twilio Segment.