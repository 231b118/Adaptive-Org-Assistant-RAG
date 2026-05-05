from flask import Flask, request, jsonify
from flask_cors import CORS
from core.database import VectorStore
from core.llm import query_mistral
import traceback

app = Flask(__name__)
CORS(app) # This prevents the "Failed to fetch" errors you saw in Brave

db = VectorStore()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    
    try:
        # 1. Search for context
        relevant_context = db.search(question, top_k=5)
        context_str = "\n".join([f"- {text}" for text in relevant_context])
        
        # 2. Get AI Response
        response = query_mistral(question, context_str)
        
        return jsonify({
            "answer": response,
            "context": context_str
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)