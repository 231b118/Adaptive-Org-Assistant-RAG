from core.ingestion import get_credentials, fetch_live_emails, fetch_calendar_events
from core.database import VectorStore
from core.llm import query_mistral


print("Starting Enterprise Org Assistant...")
db = VectorStore()
existing_ids = db.get_existing_sources()
print(f"Found {len(existing_ids)} existing records in the local database.")

print("Authenticating with Google Workspace...")
creds = get_credentials()

print("\n--- Fetching Data ---")
email_docs, email_meta = fetch_live_emails(creds, max_results=50, ignore_ids=existing_ids)
cal_docs, cal_meta = fetch_calendar_events(creds, max_results=20, ignore_ids=existing_ids)
    
all_docs = email_docs + cal_docs
all_meta = email_meta + cal_meta

if all_docs:
    print(f"\nSuccessfully pulled {len(all_docs)} NEW records ({len(email_docs)} Emails, {len(cal_docs)} Meetings).")
    print("Appending to vector and relational databases...")
    db.append_documents(all_docs, all_meta)
else:
    print("\nNo new data found. Database is up to date.")

question = "What caused the S3 403 Forbidden error, and who fixed it?"
print(f"\nUser Question: {question}")
    
print("Searching databases for context...")
try:
    relevant_context = db.search(question, top_k=10) 
    context_str = "\n".join([f"- {text}" for text in relevant_context])
        
    if not context_str.strip():
        print("No relevant context found in the database to answer this.")
    else:
        print("\n--- WHAT THE AI IS READING ---")
        print(context_str)
        print("------------------------------\n")
            
        print("Sending context to local AI...")
        query_mistral(question, context_str)
            
except ValueError as e:
    print(f"Database Error: {e}")
