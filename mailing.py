import base64
import os.path
from email.mime.text import MIMEText
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from exceptions import ServiceProviderDoesNotExistException


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class MailingService:
    def __init__(self):
        self.service = None
        # User's email address. The special value "me" can be used to indicate the authenticated user.
        self.user_id = 'me'

    def setup_mail_connection(self):
        """Authenticate to the basic service allowing to send emails programmatically via the service provider Gmail.
        This code is copied from google quickstart guide"""
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

        self.service = build('gmail', 'v1', credentials=creds)

    @staticmethod
    def _create_message(sender: str, to: str, subject: str, message_text: str) -> dict:
        """Create a message for an email.
        This code is copied from google quickstart guide.

        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.

        Returns:
          An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def _send_message(self, message):
        """Send an email message.
        This code is copied from google quickstart guide.

        Args:
          message: Message to be sent.

        Returns:
          Sent Message.
        """
        try:
            message = (self.service.users().messages().send(userId=self.user_id, body=message).execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def send_new_message(self, to: str, subject: str, message_text: str):
        """
        Toggle sending a message.

        Args:
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.

        Returns:
            None
        """
        if self.service is None:
            print("service provider does not exist")
            self.setup_mail_connection()

        msg = self._create_message('',  to, subject, message_text)
        self._send_message(msg)
