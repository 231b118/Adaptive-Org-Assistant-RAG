import requests
import json
from .config import OLLAMA_URL

def query_mistral(question, context):
    prompt = f"""
    You are an intelligent organizational assistant.
    Use ONLY the following context to answer the user's question. 
    If the answer is not in the context, state that you do not have that data.
    Note: All emails come from a shared team account. To identify the sender, ignore the 'From:' field and instead look at the Signature (e.g., - Taylor) or infer the sender by looking at who they are addressing (e.g., if it says 'Hey Sarah,' the sender is likely Marcus or Taylor).
    
    Context:
    {context}

    Question: {question}

    Answer clearly and concisely:
    """

    payload = {
        "model": "llama3.2:3b",  
        "prompt": prompt,
        "stream": False  # 🟢 SET TO FALSE for a simpler Streamlit integration
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        
        # 🟢 Extract the full response text
        result = response.json()
        full_response = result.get('response', '')
        
        # We can still keep the print for your terminal debugging
        print("\n🤖 Assistant Response (Terminal):")
        print(full_response)
        
        return full_response
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Error communicating with local LLM: {e}"
        print(error_msg)
        return error_msg