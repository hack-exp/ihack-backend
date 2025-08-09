import os
import json
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

class MedicalRAGTool:
    """
    A tool for retrieving medical information from a local FAISS vector store.
    """
    def __init__(self, data_path="Data.json", model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.data_path = data_path
        self.embed_model_name = model_name
        self.faiss_index_path = "medical_index.faiss"
        self.docs_path = "medical_docs.pkl"
        
        self.embedder = SentenceTransformer(self.embed_model_name)
        
        # Load or build the FAISS index
        self._load_or_build_index()

    def _load_or_build_index(self):
        """Loads the index if it exists, otherwise builds it."""
        if os.path.exists(self.faiss_index_path) and os.path.exists(self.docs_path):
            print("--- RAG Tool: Loading existing FAISS index and documents ---")
            self.index = faiss.read_index(self.faiss_index_path)
            with open(self.docs_path, "rb") as f:
                self.docs = pickle.load(f)
        else:
            print("--- RAG Tool: Building new FAISS index from scratch ---")
            with open(self.data_path, "r", encoding="utf-8") as f:
                dataset = json.load(f)

            self.docs = []
            for entry in dataset:
                combined_text = f"Condition: {entry['Condition']}\nSymptoms: {entry['Symptoms']}\nDrug Name: {entry['Drug_Name']}\nDosage: {entry['Dosage']}\nSide Effects: {entry['Side_Effects']}\nWarning: {entry['Warning']}"
                self.docs.append(combined_text)
            
            embeddings = self.embedder.encode(self.docs, convert_to_numpy=True)
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings)
            
            faiss.write_index(self.index, self.faiss_index_path)
            with open(self.docs_path, "wb") as f:
                pickle.dump(self.docs, f)
            print(f"--- RAG Tool: Index built and saved with {self.index.ntotal} records. ---")

    def retrieve(self, query: str, top_k: int = 3) -> str:
        """
        Encodes a query, searches the index, and returns the top_k results.
        """
        print(f"--- RAG Tool: Retrieving context for query: '{query}' ---")
        query_emb = self.embedder.encode([query], convert_to_numpy=True)
        _, indices = self.index.search(query_emb, top_k)
        results = [self.docs[i] for i in indices[0]]
        return "\n\n---\n\n".join(results)

# Create a single instance of the tool to be used by the application
# This is efficient as the index is loaded only once at startup.
medical_rag_tool = MedicalRAGTool(data_path="data/Data.json")
