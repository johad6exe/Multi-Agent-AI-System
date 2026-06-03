import os
import shutil
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.fixed import FixedSizeChunking
from RAG.knowledge import knowledge_base
from tracing.logger import sys_logger

# Ensure local directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("storage/lancedb_store", exist_ok=True)

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

        files = [f for f in os.listdir("data") if f.endswith('.pdf') or f.endswith('.md') or f.endswith('.txt')]
        if not files:
            sys_logger.warning("No files found in 'data/' to embed.")
            return

        sys_logger.info(f"Embedding documents {files} into LanceDB")
        
        # 4. Define the PDF Reader 
        pdf_reader = PDFReader(
                        chunking_strategy=FixedSizeChunking(chunk_size=1000, overlap=200),
                    )
        
        # 5. FIX: Use '.insert()' instead of '.load()'. 
        knowledge_base.insert(path="data", reader=pdf_reader) 
        
        sys_logger.info("LanceDB knowledge base successfully indexed and optimized.")
        
    except Exception as e:
        sys_logger.error(f"Critical failure initializing LanceDB RAG: {e}", exc_info=True)

if __name__ == "__main__":
    # Passing recreate=True ensures we don't duplicate vectors while testing
    initialize_knowledge_base(recreate=True)