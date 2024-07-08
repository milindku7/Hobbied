import hashlib
import uuid

def create_file(name,content):
    with open(name,"wb") as file:
        file.write(content)

def hasher():
    new_token = str(uuid.uuid4())
    new_2_token = hashlib.sha256(new_token.encode("utf-8")).hexdigest()
    return [new_token,new_2_token]

def existing_hasher(new_token):
    new_2_token = hashlib.sha256(new_token.encode("utf-8")).hexdigest()
    return new_2_token

def extract_credentials(password_str):
    password_str = password_str.replace("%21","!")
    password_str = password_str.replace("%40","@")
    password_str = password_str.replace("%23","#")
    password_str = password_str.replace("%24","$")
    password_str = password_str.replace("%2D","-")
    password_str = password_str.replace("%5F","_")
    password_str = password_str.replace("%5E","^")
    password_str = password_str.replace("%26","&")
    password_str = password_str.replace("%28","(")
    password_str = password_str.replace("%29",")")
    password_str = password_str.replace("%3D","=")
    password_str = password_str.replace("%25","%")
    return password_str

def modify_pass(password):
    salt = "76u?3uvLuy"
    password = password + salt
    password = password.encode("utf-8")
    password = hashlib.sha256(password)
    password = password.hexdigest()
    return password