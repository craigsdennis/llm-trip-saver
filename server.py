"""
Runs a Flask server to communicate with the CompanyTrip.

flask --app server run

You can submit via a POST OR GET

GET example
http://127.0.0.1:5000/company_chat?prompt=how+many+employees+are+there

See `/` for the POST example
"""

from flask import Flask, request, jsonify

from utils.trips import CompanyTrip

app = Flask(__name__)


company_name = "socimind"

company_trip = CompanyTrip.from_name(company_name)

@app.route("/")
def index():
    return f"""
    <h1>Example Flask Server</h1>
    <p>This is an example app using <code>CompanyTrip</code> bound to <strong>{company_name}</strong></p>
    <form action="/company_chat" method="post">
        <input type="text" placeholder="Enter your question" name="prompt" />
        <button type="submit">Query CompanyTrip</button>
    </form>
"""


@app.route("/company_chat", methods=["GET", "POST"])
def company_chat():
    prompt = request.values.get("prompt", "You forgot to include a prompt!")
    response = company_trip.ask(prompt)
    return jsonify(
        response=response,
        prompt=prompt,
        num_messages=len(company_trip.messages)
    )

