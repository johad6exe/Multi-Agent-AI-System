#agno imports
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.reranker.sentence_transformer import SentenceTransformerReranker

# Small, efficient and fast embedding model
embedder = SentenceTransformerEmbedder(id="BAAI/bge-small-en-v1.5")

# Knowledge base 
knowledge_base = Knowledge(
    vector_db=LanceDb(
        table_name="research_documents",
        uri="storage/lancedb_store",
        embedder=embedder,
        search_type=SearchType.hybrid,
        reranker=SentenceTransformerReranker(model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=3)
    )
)