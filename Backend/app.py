from flask import Flask,request,jsonify
from dotenv import load_dotenv
import pymongo
import os

app=Flask(__name__)

load_dotenv()

MONGO_URI=os.getenv("MONGO_URI")
client=pymongo.MongoClient(MONGO_URI)

db=client.ToDo
collection=db["ToDo_List"]

@app.route("/submittodoitem", methods=["POST"])
def submittodoitem():
    formdata=dict(request.form)
    collection.insert_one(formdata)
    return


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000,debug=True)