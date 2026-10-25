
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import pymongo
import os

app = Flask(__name__)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)

db = client.ToDo
collection = db["ToDo_List"]


@app.route("/submittodoitem", methods=["POST"])
def submittodoitem():
    formdata = request.get_json()

    task = formdata.get("task", "").strip()
    task_description = formdata.get(
        "task_description", ""
    ).strip()

    if not task or not task_description:
        return jsonify({
            "error": "Task and description are required"
        }), 400

    document = {
        "task": task,
        "task_description": task_description
    }

    result = collection.insert_one(document)

    item = {
        "item_id": str(result.inserted_id)
    }

    return jsonify({
        "message": "Data submitted successfully",
        "item": item
    }), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
