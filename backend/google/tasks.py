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
            "https://www.googleapis.com/auth/meetings.space.readonly", "https://www.googleapis.com/auth/meetings.space.created", 
            "https://www.googleapis.com/auth/drive.metadata.readonly", "https://www.googleapis.com/auth/drive.file", 'https://www.googleapis.com/auth/tasks']
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


def create_task(date):
    try:
        service = build('tasks', 'v1', credentials=creds)

        # Define the task
        task = {
            'title': 'Test Task',
            'notes': 'Description of your task',
            'due': date  # Due date and time in ISO 8601 format
        }

        # Insert the task
        task = service.tasks().insert(tasklist='@default', body=task).execute()
        
    except HttpError as error:
        print(f"An error occurred: {error}")

def main():
  authenticate_create_token()
  create_task("")

if __name__ == '__main__':
    main()