from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage
from pprint import pprint

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    return service


def send_message(service, sender, recipient, subject, message_text):
    message = EmailMessage()

    message.set_content(message_text)

    message['To'] = recipient
    message['From'] = sender
    message['Subject'] = subject

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        'raw': encoded_message
    }

    send_message = (service.users().messages().send
                    (userId="me", body=create_message).execute())
    print(F'Message Id: {send_message["id"]}')


def main():
    service = get_service()

    sender = input("Enter the sender's email address: ")
    recipient = input("Enter the recipient's email address: ")
    subject = input("Enter the subject of the email: ")
    message_text = input("Enter the text of the message: ")

    send_message(service, sender, recipient, subject, message_text)


main()