from core.ingestion import fetch_live_emails
from core.database import VectorStore
from core.llm import query_mistral

def main():
    print("Starting Enterprise Org Assistant...")

    print("Authenticating with Google Workspace...")
    docs, metadata = fetch_live_emails(max_results=15)
    
    if not docs:
        print("Exiting: No data pulled from API.")
        return

    print(f"Successfully pulled {len(docs)} live records.")

    db = VectorStore()
    print("Building vector and relational databases...")
    db.build_and_save(docs, metadata)
    
    question = "Who is overloaded this week and why?"
    print(f"\nUser Question: {question}")
    
    print("Searching databases for context...")
    relevant_context = db.search(question)
    context_str = "\n".join([f"- {text}" for text in relevant_context])

    print("Sending context to local AI...")
    query_mistral(question, context_str)

if __name__ == "__main__":
    main()