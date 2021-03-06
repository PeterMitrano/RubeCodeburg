import base64
import os
import time
import webbrowser

import httplib2
from apiclient import discovery
from email.mime.text import MIMEText
from oauth2client import client as Client
from oauth2client import tools
from oauth2client.file import Storage
from twilio.rest import Client

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def create_message(sender, to, subject, message_text):
    """Create a message for an email.
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
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    """Send an email message.
    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
    Returns:
    Sent Message.
    """
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id:' % message['id'])
        return message
    except Exception as error:
        print('An error occurred: %s' % error)


def twilio():
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = os.environ['account_sid']
    auth_token = os.environ['auth_token']

    client = Client(account_sid, auth_token)

    faxes = client.fax.v1.faxes.list()

    fax_url = 'https://s3-external-1.amazonaws.com' + faxes[0].media_url[7:]
    webbrowser.open_new_tab(fax_url)


def funfax(word='hot diggity dog'):
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http_connect = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http_connect)
    message = create_message('athenakan@college.harvard.edu', '14433399041@efaxsend.com', 'hello', word)
    send_message(service, 'athenakan@college.harvard.edu', message)
    time.sleep(80)
    twilio()


if __name__ == '__main__':
    funfax('hot diggity dog')
