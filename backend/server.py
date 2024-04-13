from flask import Flask, request, jsonify
from google.meet import authenticate_create_token

app = Flask(__name__)

@app.route("/login-test")
def login_test():
    authenticate_create_token()
    return "Login successful"

@app.route("/spaces")
def get_spaces():
    pass

@app.route("/spaces/<space_name>")
def get_space(space_name: str):
    # get the contents of a space
    # - meetings
    # - documents (later)
    auth_token = request.headers.get('Authorization')
    if not auth_token:
        return jsonify({"error": "Authorization token is missing"}), 401 

def get_space_meetings(space_name: str):
    # get the meetings a user added to a space
    pass

