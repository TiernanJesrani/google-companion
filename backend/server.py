from flask import Flask, request, jsonify
from flask_cors import CORS
from google.meet import ( 
    authenticate_create_token,
    get_events,
    get_events_with_meets,
    get_transcript_information,
    get_space,
    get_conference_records,
    get_transcripts,
    get_transcript_entries,
    get_conference_id,
    conjoin_transcript_entries
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
CORS(app)

creds = None

@app.route("/login-test")
def login_test():
    authenticate_create_token()
    return jsonify("Login successful")

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

# view the users google worksapce stuff and choose what to add to a space
@app.route("/add-to-space")
def view_workspace_entities():
    global creds
    print("Fetch events/meetings")
    authenticate_create_token()
    meetings = get_events_with_meets()
    transcript = get_transcript_information(meetings)
    #print("#meetings#", meetings)ß
    #print("#transcript#", transcript)
    return jsonify({
        "transcripts": transcript,
        "meetings": meetings
    })

# view the users' google 

@app.route("/add-space/<space_name>")
def add_space(space_name: str):
    print("Adding", space_name)
    database.add_space(space_name)
    return jsonify("Successfully added")

def create_space(space_name: str):
    # get the space information
    print("Space name", space_name)
    space = database.get_space_by_name(space_name)
    print("Retrieved space", space)
    space_name = space[1]
    space_id = space[0]
    space_description = space[2]

    # get the meetings in the space
    meetings = database.get_space_meetings(space_id)
    events = database.get_calendar_events(space_id)
    documents = database.get_documents(space_id)

    return Space(
        space_name=space_name,
        description=space_description,
        calendar_events=events,
        documents=documents,
        meetings=meetings
    )

@app.route("/get-summary/<space_name>/<meeting_id>")
def get_summary(space_name, meeting_id):

    # get the transcript information of the meeting
    global creds
    authenticate_create_token()
    events_with_meets = get_events_with_meets()
    attendees_entries = get_transcript_information(events_with_meets)

    # get the meeting id the user wants
    transcript = attendees_entries[meeting_id]
    space = create_space(space_name)
    summarizer = Companion(space)

    return jsonify([item.point for item in summarizer.summarize_meeting(transcript).main_points])


def get_space_meetings(space_name: str):
    # get the meetings a user added to a space
    pass

