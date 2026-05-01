import requests
import json
from .config import OLLAMA_URL

def query_mistral(question, context):
    prompt = f"""
    You are an intelligent organizational assistant.
    Use ONLY the following context to answer the user's question. 
    If the answer is not in the context, state that you do not have that data.

    Context:
    {context}

    Question: {question}

    Answer clearly and concisely:
    """

    payload = {
        "model": "llama3.2:1b",  
        "prompt": prompt,
        "stream": True  
    }

    try:
        # We also tell the requests library to stream the connection
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        response.raise_for_status()

        print("\n🤖 Assistant Response:")
        
        # This loop prints each word exactly as the AI thinks of it
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                word = chunk.get('response', '')
                # Print without adding a new line, and force it to the screen instantly
                print(word, end='', flush=True) 
                
        print("\n" + "="*40)
        
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with local LLM: {e}")