import faiss
import sqlite3
from sentence_transformers import SentenceTransformer
from .config import DB_PATH, FAISS_INDEX_PATH

class VectorStore:
    def __init__(self):
        # We load the embedding model here so it's ready when the class is instantiated
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None

    def build_and_save(self, documents, metadata):
        if not documents:
            print("No documents provided to the database.")
            return

        # Generate vectors
        embeddings = self.encoder.encode(documents)
        dimension = embeddings.shape[1]
        
        # Initialize and populate FAISS
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        faiss.write_index(self.index, FAISS_INDEX_PATH)

        # Initialize and populate SQLite
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents 
                (id INTEGER PRIMARY KEY, text_content TEXT, doc_type TEXT, source TEXT)
            ''')
            cursor.execute('DELETE FROM documents') # Clear old data for this run
            
            for i, text in enumerate(documents):
                doc_type = metadata[i]['type']
                source = metadata[i]['source']
                cursor.execute(
                    'INSERT INTO documents (id, text_content, doc_type, source) VALUES (?, ?, ?, ?)', 
                    (i, text, doc_type, source)
                )
            conn.commit()

    def search(self, query, top_k=3):
        if self.index is None:
            # Try to load existing index if we haven't built one in this session
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
                # FAISS returns -1 if it doesn't find enough matches
                if doc_id == -1: 
                    continue
                cursor.execute('SELECT text_content FROM documents WHERE id = ?', (int(doc_id),))
                result = cursor.fetchone()
                if result:
                    retrieved_texts.append(result[0])
                    
        return retrieved_texts