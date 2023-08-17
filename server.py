from flask import Flask, request, jsonify

from utils.trips import CompanyTrip

app = Flask(__name__)

company_trip = CompanyTrip.from_name("socimind")

@app.route("/")
def index():
    return """
    <form action="/company_chat">
        <input type="text" placeholder="Enter your question" name="prompt" />
        <button type="submit">Query CompanyTrip</button>
    </form>
"""


@app.route("/company_chat", methods=["GET", "POST"])
def company_chat():
    prompt = request.args.get("prompt", "You forgot to include a prompt!")
    response = company_trip.ask(prompt)
    return jsonify(
        response=response,
        prompt=prompt,
        num_messages=len(company_trip.messages)
    )

