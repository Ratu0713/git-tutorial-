
from flask import Flask, request, render_template
import requests

app = Flask(__name__)
BACKEND_URL = 'http://127.0.0.1:9000'


@app.route("/")
def dashboardFrom():
    return render_template('index.html')


@app.route("/submittodoitem", methods=["POST"])
def submittodoitem():
    formdata = dict(request.form)

    response = requests.post(
        BACKEND_URL + "/submittodoitem",
        json=formdata
    )
    response.raise_for_status()

    result = response.json()

    return render_template(
        'index.html',
        item=result["item"],
        message="Data submitted successfully"
    )


if __name__ == '__main__':
    app.run(port=8000, debug=True)
