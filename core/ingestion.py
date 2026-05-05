import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from .config import SCOPES, CREDENTIALS_PATH, TOKEN_PATH

def get_credentials():
    """Gets valid user credentials from storage or initiates OAuth2 flow."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0, prompt='select_account')
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return creds

import base64

def fetch_live_emails(creds, max_results=50, ignore_ids=None):
    # Connects to Gmail API and extracts the plain text from your latest emails
    try:
        if ignore_ids is None:
            ignore_ids = set()
            
        # 1. Use the shared credentials here!
        service = build('gmail', 'v1', credentials=creds)
        
        # 🟢 NEW: Announce the fetch attempt
        print(f"Fetching up to {max_results} recent emails from Gmail...")
        
        results = service.users().messages().list(userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])

        unified_documents = []
        metadata_store = []

        if not messages:
            print("No new messages found.")
            return [], []

        for msg in messages:
            msg_id = msg['id']
        
            # 🚀 THE MAGIC FILTER: Skip if we already have it!
            if msg_id in ignore_ids:
                continue
                
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = msg_data.get('payload', {})
            headers = payload.get('headers', [])
            
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
            from_header = next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown Sender')
            sender_name = from_header.split('<')[0].strip() if '<' in from_header else from_header
            
            body = ""
            if 'parts' in payload:
                for part in payload['parts']:
                    if part.get('mimeType') == 'text/plain':
                        data = part['body'].get('data')
                        if data:
                            body = base64.urlsafe_b64decode(data).decode('utf-8')
                            break

            clean_body = body.replace('\r', '').replace('\n', ' ').strip()
            
            formatted_text = f"[EMAIL] Author: {sender_name} | Subject: {subject} | Body: {clean_body[:500]}"
            unified_documents.append(formatted_text)
            
            # 2. CRITICAL FIX: Save msg_id as the source so the ignore filter works!
            metadata_store.append({"type": "email", "source": msg_id})
            
        # 🟢 NEW: Announce exactly how many fresh emails were processed
        print(f"Processed {len(unified_documents)} new emails for the database.")
        
        return unified_documents, metadata_store

    except Exception as e:
        print(f"Error communicating with Google API: {e}")
        return [], []
    
import datetime
from googleapiclient.discovery import build

def fetch_calendar_events(creds, max_results=20, ignore_ids=None):
    """Fetches calendar events and formats them for the vector database."""
    if ignore_ids is None:
        ignore_ids = set()
        
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        now = '2026-05-01T00:00:00Z' 
        
        print(f"Fetching up to {max_results} upcoming calendar events...")
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=now,
            maxResults=max_results, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        docs = []
        metadata = []
        
        if not events:
            return docs, metadata
            
        for event in events:
            event_id = event['id']
            
            if event_id in ignore_ids:
                continue
                
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            summary = event.get('summary', 'No Title')
            description = event.get('description', 'No Description')
            attendees = [a.get('email') for a in event.get('attendees', [])]
            
            # Format the text so the LLM understands it's a meeting
            text_content = (
                f"Meeting: {summary}\n"
                f"Start: {start}\n"
                f"End: {end}\n"
                f"Attendees: {', '.join(attendees) if attendees else 'None listed'}\n"
                f"Details: {description}"
            )
            
            docs.append(text_content)
            metadata.append({'type': 'calendar', 'source': event_id})
            
        return docs, metadata

    except Exception as error:
        print(f"An error occurred fetching calendar events: {error}")
        return [], []