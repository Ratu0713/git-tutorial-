
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import pymongo

app = Flask(__name__)

load_dotenv()

MONGO_URL = os.getenv("MONGO_URI")

if not MONGO_URL:
    raise ValueError("MONGO_URI is missing from .env")

client = pymongo.MongoClient(
    MONGO_URL,
    serverSelectionTimeoutMS=5000
)

db = client["task"]
collection = db["API_RESPONSE_COLLECTION"]


@app.route("/submit", methods=["POST"])
def submit():
    try:
        form_data = request.get_json(silent=True)

        if not isinstance(form_data, dict) or not form_data:
            return jsonify({"error": "No valid form data received"}), 400

        collection.insert_one(form_data)

        return jsonify({
            "message": "Data submitted successfully"
        }), 201

    except pymongo.errors.PyMongoError:
        app.logger.exception("MongoDB insertion failed")
        return jsonify({
            "error": "Failed to save data to MongoDB"
        }), 500


@app.route("/api", methods=["GET"])
def json_list():
    try:
        data = list(collection.find({}, {"_id": 0}))
        return jsonify({"data": data}), 200

    except pymongo.errors.PyMongoError:
        return jsonify({"error": "Failed to fetch data"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=False)
