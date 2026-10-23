
from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)

BACKEND_URL = "http://127.0.0.1:9000"


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        form_data = request.form.to_dict()

        if not form_data:
            return render_template(
                "index.html",
                error="Please fill in the form."
            ), 400

        response = requests.post(
            BACKEND_URL + "/submit",
            json=form_data,
            timeout=5
        )

        response.raise_for_status()

        # Success: redirect to the dedicated success page
        return redirect(url_for("success"), code=303)

    except requests.RequestException:
        # Error: remain on the form page
        return render_template(
            "index.html",
            error="Data could not be submitted. Please try again."
        ), 500


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/get_data")
def get_data():
    try:
        response = requests.get(
            BACKEND_URL + "/api",
            timeout=5
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        return {"error": "Could not fetch data"}, 502


if __name__ == "__main__":
    app.run(port=8000, debug=True)
