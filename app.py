from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
import pymongo

app = Flask(__name__)

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)

db=client.test
collection=db['flusk_collection']

@app.route("/api")
def userDetails():
    name = request.values.get('name')
    age = request.values.get('age')

    age = int(age)

    details = {
        'name': name,
        'age': age
    }

    if age > 18:
        details["message"] = "you can vote"
    else:
        details["message"] = "you cannot vote"

    return details


@app.route("/")
def dashboard():
    return render_template('index.html')


# @app.route('/submit', methods=['POST'])
# def submit():
#     form_data = dict(request.form)
#     print(form_data)
#     return form_data

@app.route('/submit',methods=['POST'])
def submit():
    name=request.form.get('name')
    
    formData=dict(request.form)
    collection.insert_one(formData)
    return "successfully inserted"
@app.route('/view')
def view():
    data=collection.find()
    listData=list(data)
    for item in listData:
        del item['_id']
    result={
        'data':listData
    }
    return result
if __name__ == '__main__':
    app.run(debug=True)