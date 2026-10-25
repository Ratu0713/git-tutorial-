from flask import Flask,request,render_template
import requests
app=Flask(__name__)
BACKEND_URL='http://0.0.0.0:9000'


@app.route("/")
def dashboardFrom():
    return render_template('index.html')

@app.route("/submittodoitem",methods=["POST"])
def submittodoitem():
    formdata=dict(request.form)
    requests.post(BACKEND_URL+"/submit",json=formdata)
    return "Data submitted successfully"
    

if __name__=='__main__':
    app.run(port=8000,debug=True)
    