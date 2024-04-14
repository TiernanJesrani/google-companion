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
    conjoin_transcript_entries,
)
from google.docs import (
    authenticate_and_create_token_1,
    retrieve_doc_ids,
    get_doc_content
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

# working
@app.route("/login-test")
def login_test():
    global creds
    print("before")
    authenticate_create_token()
    print('after')
    return jsonify("Login successful")

# not being used
@app.route("/spaces")
def get_spaces():
    global creds
    print("before")
    authenticate_create_token()
    spaces = database.get_spaces()
    return jsonify(spaces)


# working
@app.route("/spaces/<space_name>")
def get_space(space_name: str):
    # get the contents of a space
    # - meetings
    # - calendar events
    # - documents (later)
    global creds
    print("before")
    authenticate_create_token()
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

# view the users' google drive and choose which docs to add
@app.route("/add-docs-to-space")
def add_docs_to_space():
    global creds

    authenticate_and_create_token_1()
    document_id_name_webViewLink = retrieve_doc_ids()
    
    return document_id_name_webViewLink

@app.route("/add-space/<space_name>")
def add_space(space_name: str):
    global creds
    print("before")
    authenticate_create_token()
    print("Adding", space_name)
    database.add_space(space_name)
    return jsonify("Successfully added")

def create_space(space_name: str):
    # get the space information
    global creds
    print("before")
    authenticate_create_token()
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

# working
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

chat_companion = None

# just wrote it - working?
@app.route("/<space_name>/chat")
def get_response(space_name):
    global creds
    print("before")
    authenticate_create_token()
    global chat_companion
    query = request.args.get('query')
    if not chat_companion:
        space = create_space(space_name)
        chat_companion = ChatCompanion(space)
    # use chat_companion
    response = chat_companion(query, with_retrieval=True)
    return response

