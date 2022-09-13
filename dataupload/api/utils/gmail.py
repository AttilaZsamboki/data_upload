from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os

SCOPES = ["https://mail.google.com/"]
our_email = "gds.dataupload@gmail.com"


def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("/home/atti/googleds/dataupload/api/token.pickle"):
        with open("/home/atti/googleds/dataupload/api/token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/atti/googleds/dataupload/api/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("/home/atti/googleds/dataupload/api/token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


# get the Gmail API service
service = gmail_authenticate()


def build_message(destination, obj, body, attachments=[]):
    if not attachments:  # no attachments given
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = our_email
        message['subject'] = obj
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, destination, obj, body, attachments=[]):
    return service.users().messages().send(
        userId="me",
        body=build_message(destination, obj, body, attachments)
    ).execute()
