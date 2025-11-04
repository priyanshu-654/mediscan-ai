import json
from passlib.hash import pbkdf2_sha256
import jwt
import datetime

# JWT secret key
SECRET_KEY = "your_secret_key_here"

USERS_FILE = "users.json"

# ---------------- USER STORAGE ----------------
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------------- REGISTER USER ----------------
def register_user(username, password, email=None):
    users = load_users()
    if username in users:
        return False, "User already exists"
    hashed = pbkdf2_sha256.hash(password)
    users[username] = {"password": hashed, "email": email}
    save_users(users)
    return True, "Registration successful"

# ---------------- VERIFY USER ----------------
def verify_user(username, password):
    users = load_users()
    if username not in users:
        return False, "User does not exist"
    hashed = users[username]["password"]
    if pbkdf2_sha256.verify(password, hashed):
        return True, "Login successful"
    return False, "Incorrect password"

# ---------------- JWT TOKEN ----------------
def create_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True, payload["username"]
    except jwt.ExpiredSignatureError:
        return False, "Token expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"