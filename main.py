from flask import Flask, render_template, request, jsonify, redirect, make_response
import json
from pymongo import MongoClient
import re
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__,template_folder="public")

mongo_client = MongoClient("mongo")
db = mongo_client["hobbied"]
posts = db["posts"]
users = db["users"]    

def check_email(email):
    try:
      # validate and get info
        v = validate_email(email) 
        # replace with normalized form
        email = v["email"]  
        return True
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        return False

def validate_password(password):
    

@app.route("/")
def serve_index():
    return render_template("login.html")

@app.route("/signup")
def serve_signup():
    return make_response(render_template("signup.html"))

@app.route("/signup/signup_details",methods=["POST"])
def after_signup():
    req_json = request.get_json()
    email = req_json["email"]
    email_result = check_email(email)
    if email_result is False:
        data = {
        "message": "email"
        }
        return jsonify(data)
    password = req_json
    password_result = validate_password(password)

    data = {
        "message": req_json["password"]
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port=8080)