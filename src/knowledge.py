# src/knowledge.py
import os
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.duckdb import DuckDb
# Use local embeddings to demonstrate cost-efficiency and privacy
from agno.embedder.sentence_transformers import SentenceTransformerEmbedder
from src.logger import sys_logger

os.makedirs("data", exist_ok=True)
os.makedirs("storage", exist_ok=True)

sys_logger.info("Configuring State-of-the-Art RAG Pipeline...")

# 1. Explicit Embedder: 'all-MiniLM-L6-v2' is the industry standard for fast, high-quality local RAG
embedder = SentenceTransformerEmbedder(model_name="all-MiniLM-L6-v2")

# 2. Advanced Knowledge Base Configuration
knowledge_base = PDFKnowledgeBase(
    path="data",
    vector_db=DuckDb(
        table_name="research_documents",
        db_path="storage/vector_store.db",
        embedder=embedder,
    ),
    # 3. Explicit Chunking Strategy: 
    # 1000 chars gives enough context for the LLM, 200 overlap prevents cutting sentences in half.
    chunk_size=1000,
    chunk_overlap=200,
    # 4. Search Optimization: Retrieve the top 5 most relevant chunks (default is often too low)
    num_documents=5 
)

def initialize_knowledge_base(recreate: bool = False):
    
    # Ingests documents into the vector database.
    
    try:
        files = [f for f in os.listdir("data") if f.endswith('.pdf')]
        if not files:
            sys_logger.warning("No PDF files found in 'data/' to embed.")
            return

        sys_logger.info(f"Embedding documents {files} using local SentenceTransformers...")
        
        # Load and embed the documents
        knowledge_base.load(recreate=recreate) 
        
        sys_logger.info("Knowledge base optimized and ready for querying.")
        
    except Exception as e:
        sys_logger.error(f"Critical failure initializing RAG: {e}", exc_info=True)

if __name__ == "__main__":
    # Passing recreate=True during testing ensures you don't get duplicate vectors
    initialize_knowledge_base(recreate=True)