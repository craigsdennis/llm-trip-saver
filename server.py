from flask import Flask, request, jsonify

from utils.trips import CompanyTrip

app = Flask(__name__)

company_trip = CompanyTrip.from_name("socimind")

@app.route("/company_chat")
def company_chat():
    prompt = request.args["prompt"]
    return jsonify(
        response=company_trip.ask(prompt),
        prompt=prompt,
    )