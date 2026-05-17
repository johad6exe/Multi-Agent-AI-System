# src/knowledge.py
import os
import shutil
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from src.logger import sys_logger

# Ensure local directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("storage/lancedb_store", exist_ok=True)

sys_logger.info("Configuring State-of-the-Art LanceDB RAG Pipeline...")

# 1. Initialize the Local Embedder
embedder = SentenceTransformerEmbedder(id="all-MiniLM-L6-v2")

# 2. Configure LanceDB Vector Store (Hybrid Search enabled)
vector_db = LanceDb(
    table_name="research_documents",
    uri="storage/lancedb_store",
    embedder=embedder,
    search_type=SearchType.hybrid,
)

# 3. Configure the Knowledge Base
knowledge_base = Knowledge(
    vector_db=vector_db
)

def initialize_knowledge_base(recreate: bool = False):
    """
    Ingests documents into the LanceDB vector database and builds the index.
    """
    try:
        # Safely wipe the local storage if we want a fresh start
        if recreate and os.path.exists("storage/lancedb_store"):
            sys_logger.info("Recreate flag passed: Wiping old LanceDB vectors for a clean build...")
            shutil.rmtree("storage/lancedb_store")
            os.makedirs("storage/lancedb_store", exist_ok=True)

        files = [f for f in os.listdir("data") if f.endswith('.pdf')]
        if not files:
            sys_logger.warning("No PDF files found in 'data/' to embed.")
            return

        sys_logger.info(f"Embedding documents {files} into LanceDB using Hybrid Search...")
        
        # 4. Define the PDF Reader 
        pdf_reader = PDFReader(chunk=True, chunk_size=1000, chunk_overlap=200)
        
        # 5. FIX: Use '.insert()' instead of '.load()'. 
        knowledge_base.insert(path="data", reader=pdf_reader) 
        
        sys_logger.info("LanceDB knowledge base successfully indexed and optimized.")
        
    except Exception as e:
        sys_logger.error(f"Critical failure initializing LanceDB RAG: {e}", exc_info=True)

if __name__ == "__main__":
    # Passing recreate=True ensures we don't duplicate vectors while testing
    initialize_knowledge_base(recreate=True)