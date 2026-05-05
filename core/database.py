import faiss
import sqlite3
import os
from sentence_transformers import SentenceTransformer
from .config import DB_PATH, FAISS_INDEX_PATH

class VectorStore:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None

    def get_existing_sources(self):
        """Returns a set of all email IDs (sources) currently in the database."""
        if not os.path.exists(DB_PATH):
            return set()
            
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Check if table exists first
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents'")
            if not cursor.fetchone():
                return set()
                
            # Fetch all existing source IDs
            cursor.execute('SELECT source FROM documents')
            return set(row[0] for row in cursor.fetchall())

    def append_documents(self, documents, metadata):
        if not documents:
            print("No new documents to add to the database.")
            return

        # 1. Load existing FAISS index or create a new one
        try:
            self.index = faiss.read_index(FAISS_INDEX_PATH)
            start_id = self.index.ntotal  # Get the current number of vectors
        except Exception:
            # If no index exists, create one
            sample_embedding = self.encoder.encode([documents[0]])
            dimension = sample_embedding.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            start_id = 0  # Starting fresh

        # 2. Embed and add new vectors to FAISS
        print(f"Embedding {len(documents)} new documents...")
        embeddings = self.encoder.encode(documents)
        self.index.add(embeddings)
        faiss.write_index(self.index, FAISS_INDEX_PATH)

        # 3. Append metadata to SQLite without deleting old data
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents 
                (id INTEGER PRIMARY KEY, text_content TEXT, doc_type TEXT, source TEXT)
            ''')
            # NOTE: We removed the 'DELETE FROM documents' command!
            
            for i, text in enumerate(documents):
                doc_type = metadata[i]['type']
                source = metadata[i]['source'] # Ensure this contains the unique Gmail Message ID
                
                # We align the SQLite ID with the FAISS internal index ID (start_id + i)
                cursor.execute(
                    'INSERT INTO documents (id, text_content, doc_type, source) VALUES (?, ?, ?, ?)', 
                    (start_id + i, text, doc_type, source)
                )
            conn.commit()
            print(f"Successfully appended {len(documents)} records. Total database size: {self.index.ntotal}")

    def search(self, query, top_k=3):
        if self.index is None:
            try:
                self.index = faiss.read_index(FAISS_INDEX_PATH)
            except Exception:
                raise ValueError("FAISS index not found. Build the database first.")

        query_vector = self.encoder.encode([query])
        distances, indices = self.index.search(query_vector, top_k)

        retrieved_texts = []
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for doc_id in indices[0]:
                if doc_id == -1: 
                    continue
                cursor.execute('SELECT text_content FROM documents WHERE id = ?', (int(doc_id),))
                result = cursor.fetchone()
                if result:
                    retrieved_texts.append(result[0])
                    
        return retrieved_texts