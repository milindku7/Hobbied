from flask import Flask, render_template, request, jsonify, redirect, make_response
import json
from pymongo import MongoClient

app = Flask(__name__,template_folder="public")

mongo_client = MongoClient("mongo")
db = mongo_client["hobbied"]
posts = db["posts"]
users = db["users"]    

@app.route("/")
def serve_index():
    return render_template("login.html")

@app.route("/signup")
def serve_signup():
    return make_response(render_template("signup.html"))

@app.route("/signup/signup_details",methods=["POST"])
def after_signup():
    print(request)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port=8080)