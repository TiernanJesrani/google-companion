from flask import Flask, request, jsonify
from google.meet import ( 
    authenticate_create_token,
    get_events,
    get_events_with_meets,
    get_transcript_information,
)
from llm.companion import (
    Companion,
    ChatCompanion,
    Response
)
from llm.schemas import (
    Document,
    CalendarEvent,
    Meeting,
    Space
)
import database

app = Flask(__name__)

@app.route("/login-test")
def login_test():
    authenticate_create_token()
    return "Login successful"

@app.route("/spaces")
def get_spaces():
    spaces = database.get_spaces()
    return jsonify(spaces)

@app.route("/spaces/<space_name>")
def get_space(space_name: str):
    # get the contents of a space
    # - meetings
    # - calendar events
    # - documents (later)
    space = database.get_space_from_name(space_name)

    # get the meetings in the space
    space_id = space["id"]
    meetings = database.get_space_meetings(space_id)
    events = database.get_space_events(space_id)

    return jsonify({
        "meetings": meetings,
        "events": events
    })

@app.route("/add")
def view_workspace_entities():
    events = get_events()
    meetings = get_events_with_meets()

    return jsonify({
        "events": events,
        "meetings": meetings
    })


def get_space_meetings(space_name: str):
    # get the meetings a user added to a space
    pass

