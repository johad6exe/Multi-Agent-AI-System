import os
import shutil
import lancedb
#agno imports
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.document import DocumentChunking
#module imports
from RAG.knowledge import knowledge_base
from tracing.logger import sys_logger

#ingests docs into VectorDB and builds the index
def initialize_knowledge_base(recreate: bool = False):
    try:
        os.makedirs("data", exist_ok=True)
        files = [f for f in os.listdir("data") if f.endswith('.pdf') or f.endswith('.md') or f.endswith('.txt')]
        if not files:
            sys_logger.warning("Files not found in target directory.")
            return

        # Safely wipe the local storage if we want a fresh start
        if recreate and os.path.exists("storage/lancedb_store"):
            sys_logger.info("Recreate flag passed: Wiping old LanceDB vectors for a clean build...")
            shutil.rmtree("storage/lancedb_store")
            os.makedirs("storage/lancedb_store", exist_ok=True)
        
        sys_logger.info(f"Embedding documents {files} into LanceDB")
        
        pdf_reader = PDFReader(
                        chunking_strategy=DocumentChunking(chunk_size=500, overlap=100),
                    )
        knowledge_base.insert(path="data", reader=pdf_reader)
        
        # Building native Full-Text Search index for true keyword-matching fallback
        sys_logger.info("Building Full-Text Search index for hybrid retrieval...")
        db = lancedb.connect("storage/lancedb_store")
        table = db.open_table("research_documents")
        table.create_fts_index("payload", replace=True)
         
        sys_logger.info("LanceDB knowledge base successfully indexed and optimized.")
        
    except Exception as e:
        sys_logger.error(f"Critical failure initializing LanceDB RAG: {e}", exc_info=True)

if __name__ == "__main__":
    # Passing recreate=True ensures we don't duplicate vectors while testing
    initialize_knowledge_base(recreate=True)