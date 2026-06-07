from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
# module import
from config import embedder, reranker

# Knowledge base 
knowledge_base = Knowledge(
    vector_db=LanceDb(
        table_name="research_documents",
        uri="storage/lancedb_store",
        embedder=embedder,
        search_type=SearchType.hybrid,
        reranker= reranker
    )
)