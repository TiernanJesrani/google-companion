from __future__ import print_function
import datetime
import os.path

from google.apps import meet_v2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

creds = None

def authenticate_create_token():
   # If modifying these scopes, delete the file token.json.
  SCOPES = ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/drive.readonly", 
            "https://www.googleapis.com/auth/meetings.space.readonly", "https://www.googleapis.com/auth/meetings.space.created"]
  global creds
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  


def get_conference_id(event):
  data = event["conferenceData"]
  return data["conferenceId"]



# get all events, whether they have meetings or don't
def get_events():
  try:
    global creds
    # create calendar service 
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    # Get current UTC time
    current_utc_time = datetime.datetime.utcnow()

    # Define UTC timezone
    utc_timezone = datetime.timezone.utc

    # Convert UTC time to Eastern Standard Time (EST) by adding 5 hours (UTC-5)
    est_timezone_offset = datetime.timedelta(hours=-5)
    current_est_time = current_utc_time.replace(tzinfo=utc_timezone) + est_timezone_offset

    # Subtract a week from the current date
    one_week_ago = current_est_time - datetime.timedelta(days=7)

    # Format the result in ISO 8601 format
    one_week_ago_iso = one_week_ago.isoformat()

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=one_week_ago_iso,
            maxResults=30,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    
    events = events_result.get("items", [])
 
    if not events:
      print("No events found.")
      return

    return events

  except HttpError as error:
    print(f"An error occurred: {error}")



# get all events with meetings
def get_events_with_meets():
  # get all events
  events = get_events()

  events_with_meets = []
  for event in events:
      if "hangoutLink" in event:
        events_with_meets.append(event)
  
  return events_with_meets


def get_transcript_information(events):
  # dict of transcript info for each selected meeting
  transcript_info = {}
  for event in events:
    # get the space associated with an event
    space = get_space(event)
  
    # get the records associated with that space
    conference_records = get_conference_records(space)
    
    if len(conference_records) == 0:
      print("empty")
    else:
    # get all the transcripts for all the records
      transcripts = get_transcripts(conference_records)
      
      if len(transcripts) == 0:
        print("transcripts empty")

      else:
      # get all the transcript entries for all the transcripts
        transcript_entries = get_transcript_entries(transcripts)

        transcript_info[get_conference_id(event)] = conjoin_transcript_entries(transcript_entries)
    
  return transcript_info

    
    



# get a space for an event
def get_space(event):
  
  try:
    global creds
    # create space client
    client_space = meet_v2.SpacesServiceClient(credentials=creds)

    conf_id = get_conference_id(event)
    request = meet_v2.GetSpaceRequest(
      name=f"spaces/{conf_id}"
    )
    
    return client_space.get_space(request=request)
  
  except HttpError as error:
    print(f"An error occurred: {error}")
    
  
# get all the conference records for a space
def get_conference_records(space):
  try:
    global creds
    # create transcript client
    client_rec = meet_v2.ConferenceRecordsServiceClient(credentials=creds)

    conference_records = []
    request = meet_v2.ListConferenceRecordsRequest()
    records = client_rec.list_conference_records(request=request)
    
    for record in records:
      if record.space == space.name:
          conference_records.append(record.name)
    

    return conference_records
  
  except HttpError as error:
    print(f"An error occurred: {error}")



# get all the transcripts for a conference record 
def get_transcripts(conference_records):
  try:
    global creds
    # create transcript client
    client_rec = meet_v2.ConferenceRecordsServiceClient(credentials=creds)
    
    transcripts = []
    for record in conference_records:
      request = meet_v2.ListTranscriptsRequest(
        parent=record
      ) 
      transcripts_for_one_conference = client_rec.list_transcripts(request=request)
      if not transcripts_for_one_conference.transcripts:
        return []
      
      else:
        for transcript in transcripts_for_one_conference:
          transcripts.append(transcript)
        return transcripts
  
  except HttpError as error:
    print(f"An error occurred: {error}")

# get all the transcript entries
def get_transcript_entries(transcripts):
  try:
    global creds
    # create transcript client
    client_rec = meet_v2.ConferenceRecordsServiceClient(credentials=creds)

    transcript_entries = []
    
    for transcript in transcripts:
      request = meet_v2.ListTranscriptEntriesRequest(
        parent=transcript.name,
      )
      transcript_entries_for_one_transcript = client_rec.list_transcript_entries(request=request)

      transcript_entries.extend(transcript_entries_for_one_transcript)
    
    return transcript_entries

  except HttpError as error:
    print(f"An error occurred: {error}")



def conjoin_transcript_entries(transcript_entries):
  global creds
  # create transcript client
  client_rec = meet_v2.ConferenceRecordsServiceClient(credentials=creds)

  curr_participant = transcript_entries[0].participant

  attendees = []
  entries = []
  text = ""

  request_pariticpant_individual = meet_v2.GetParticipantRequest(
        name=curr_participant
  )

  for entry in transcript_entries:
    if curr_participant != "" and curr_participant != entry.participant:
      request_pariticpant_individual = meet_v2.GetParticipantRequest(
        name=curr_participant
      )
      participant = client_rec.get_participant(request=request_pariticpant_individual)

      if participant not in attendees:
        attendees.append(participant)

      text = f"{participant.signedin_user.display_name}: " + text
      entries.append(text)
      text = ""
      curr_participant = entry.participant
    text = text + entry.text
  

  request_pariticpant_individual = meet_v2.GetParticipantRequest(
    name=curr_participant
  )
  participant = client_rec.get_participant(request=request_pariticpant_individual)

  if participant not in attendees:
    attendees.append(participant)

  text = f"{participant.signedin_user.display_name}: " + text
  entries.append(text)

  attendee_entry = []
  attendee_entry.append(attendees)
  attendee_entry.append(entries)
  return entries


def main():
  authenticate_create_token()
  events = get_events()
  print(events)

  events_with_meets = get_events_with_meets()
  attendees_entries = get_transcript_information(events_with_meets)
  print(attendees_entries)


if __name__ == '__main__':
    main()

#https://developers.google.com/meet/api/reference/rest/v2
#https://developers.google.com/docs/api/samples/extract-text#python
# meet.google.com/uvv-uoby-hop