# src/knowledge.py
import os
import shutil
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.reranker.sentence_transformer import SentenceTransformerReranker

# 1. Initialize the Local Embedder
embedder = SentenceTransformerEmbedder(id="BAAI/bge-small-en-v1.5")

# 2. Configure the Knowledge Base
knowledge_base = Knowledge(
    vector_db=LanceDb(
        table_name="research_documents",
        uri="storage/lancedb_store",
        embedder=embedder,
        search_type=SearchType.hybrid,
        reranker=SentenceTransformerReranker(model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=3)
    )
)