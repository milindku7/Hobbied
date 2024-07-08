from flask import Flask, render_template, request, jsonify, redirect, make_response
import json
from pymongo import MongoClient
import re
from email_validator import validate_email, EmailNotValidError
import helper.auth
import hashlib
import uuid

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
    specials = ["!","@","#","$","%","^","&","(",")","-","_","="]
    if len(password) > 7:
        l = 0
        u = 0
        n = 0
        s = 0
        i = 0
        for char in password:
            if char.isnumeric():
                n = n + 1
            elif char in specials:
                s = s + 1
            elif char.islower():
                l = l + 1
            elif char.isupper():
                u = u + 1
            else:
                i = i + 1
        
        if l > 0 and u > 0 and n > 0 and s > 0 and i == 0:
            return True
    return False

def escape_characters(username):
    username = username.replace("&","&amp;")
    username = username.replace("<","&lt;")
    username = username.replace(">","&gt;")
    return username

def validate_username(username):
    username = escape_characters(username)
    user_found = users.find_one({"username": username})
    if user_found is None:
        return True
    else:
        return False

@app.route("/")
def serve_index():
    if "auth_token" in request.cookies.keys():
        auth_token = request.cookies.get("auth_token")
        auth_token = helper.auth.existing_hasher(auth_token)
        found_auth_token = users.find_one({"authtoken": auth_token})
        if found_auth_token:
            xsrf = str(found_auth_token["XSRF"])
            return render_template("index.html",XSRF_value=xsrf,Username_status=True,Username=found_auth_token["username"],postsInfo=posts.find())
        else:
            return render_template("index.html",Username_status=False,postsInfo=posts.find())
    else:
        return render_template("index.html",Username_status=False,postsInfo=posts.find())

@app.route("/signup")
def serve_signup():
    return make_response(render_template("signup.html"))

@app.route("/signup/signup_details",methods=["POST"])
def after_signup():
    req_json = request.get_json()
    email = helper.auth.extract_credentials(req_json["email"])
    email_result = check_email(email)
    
    if email_result is False:
        data = {
        "message": "email"
        }
        return jsonify(data)
    
    password = helper.auth.extract_credentials(req_json["password"])
    password_result = validate_password(password)
    password = helper.auth.modify_pass(password)

    if password_result is False:
        data = {
        "message": "password"
        }
        return jsonify(data)
    
    username = helper.auth.extract_credentials(req_json["username"])
    username_result = validate_username(username)
    
    if username_result is False:
        data = {
        "message": "username"
        }
        return jsonify(data)
    
    users.insert_one({"username": username, "password": password, "authtoken": "", "XSRF": ""})
    data = {
        "message": "allright"
    }
    return jsonify(data)

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/login/login_details",methods=["POST"])
def check_login():
    req_json = request.get_json()
    username = req_json["username"]
    username = helper.auth.extract_credentials(username)
    username = escape_characters(username)
    found_user = users.find_one({"username": username})
    if found_user:
        received_pass = req_json["password"]
        received_pass = helper.auth.extract_credentials(received_pass)
        received_pass = helper.auth.modify_pass(received_pass)
        og_pass = found_user["password"]
        if og_pass == received_pass:
            data = {
            "message": "allright"
            }
            
            auther = helper.auth.hasher()
            users.update_one({"username": username},{"$set" : {"authtoken": auther[1]}})
            
            new_xsrf = uuid.uuid4()
            new_xsrf = str(new_xsrf)
            users.update_one({"username": username},{"$set" : {"XSRF": new_xsrf}})
            
            response = make_response(jsonify(data))
            response.set_cookie("auth_token",auther[0],max_age=31536000,httponly=True,secure=True)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response
    else:
        data = {
            "message": "notright"
        }
        return jsonify(data)

@app.route("/new_post",methods=["POST"])
def create_new_post():
    req_json = request.get_json()
    xsrf = req_json["XSRF"]
    xsrf = helper.auth.extract_credentials(xsrf)
    xsrf = escape_characters(xsrf)
    found_user = users.find_one({"XSRF": xsrf})
    if found_user:
        auth = request.cookies.get("auth_token")
        if auth == found_user["authtoken"]:
            title  = req_json["title"]
            title = helper.auth.extract_credentials(title)
            title = escape_characters(title)
            
            desc  = req_json["description"]
            desc = helper.auth.extract_credentials(desc)
            desc = escape_characters(desc)
            
            image_data = req_json["picture"]
            image_name = str(uuid.uuid4())
            image_name = "/static/images/" + image_name
            helper.auth.create_file(image_name,image_data)
            
            id = str(uuid.uuid4())
            
            posts.insert_one({"title":title,"description":desc,"id":id,"image_src":image_name})
            return jsonify({"message":"done"})

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port=8080)