from __future__ import print_function
import datetime
import os.path

from google.apps import meet_v2
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

creds = None

def authenticate_and_create_token_1():
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


# gets the user's file names, ids, and links to view the documents
def retrieve_doc_ids():
    global creds
    try:

        drive_service = build('drive', 'v3', credentials=creds)

        response = drive_service.files().list(q="mimeType='application/vnd.google-apps.document'",
                                      fields='files(id, name, webViewLink)').execute()
        files = response.get('files', [])

        return files

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")

# returns the requested documents' content in a list
def get_doc_content(doc_ids):
    global creds
    try:
        
        document_list = []
        docs_service = build('docs', 'v1', credentials=creds)
        for doc in doc_ids:
            document_data = docs_service.documents().get(documentId=doc['id']).execute()
            response = document_data.get('body').get('content')
            content = ""
            for item in response:
                if 'paragraph' in item:
                    elements = item['paragraph']['elements']
                    for element in elements:
                        if 'textRun' in element:
                            content += element['textRun']['content']
                


            document_list.append(content)

        return document_list

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")

def main():
    authenticate_and_create_token_1()
    document_ids = retrieve_doc_ids()
    document_list = get_doc_content(document_ids)
    #print(document_list)


if __name__ == '__main__':
    main()


# Assuming you have already authenticated and have your credentials
# stored in `creds` variable
