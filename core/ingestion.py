import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from .config import SCOPES, CREDENTIALS_PATH, TOKEN_PATH

def authenticate_gmail():
    # Handles OAuth2 login. Generates a token.json file so you only have to log in once.
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
            
    return build('gmail', 'v1', credentials=creds)

def fetch_live_emails(max_results=5):
    # Connects to Gmail API and extracts the plain text from your latest emails
    try:
        service = authenticate_gmail()
        results = service.users().messages().list(userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])

        unified_documents = []
        metadata_store = []

        if not messages:
            print("No new messages found.")
            return [], []

        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = msg_data.get('payload', {})
            headers = payload.get('headers', [])
            
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
            sender = next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown Sender')
            
            # Extract body text
            body = ""
            if 'parts' in payload:
                for part in payload['parts']:
                    if part.get('mimeType') == 'text/plain':
                        data = part['body'].get('data')
                        if data:
                            body = base64.urlsafe_b64decode(data).decode('utf-8')
                            break

            clean_body = body.replace('\r', '').replace('\n', ' ').strip()
            
            formatted_text = f"[EMAIL] From: {sender} | Subject: {subject} | Body: {clean_body[:500]}"
            unified_documents.append(formatted_text)
            metadata_store.append({"type": "email", "source": sender})
            
        return unified_documents, metadata_store

    except Exception as e:
        print(f"Error communicating with Google API: {e}")
        return [], []