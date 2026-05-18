from ddgs import DDGS
import numpy as np
from sentence_transformers import CrossEncoder
from src.knowledge import knowledge_base
from src.logger import sys_logger
from src.knowledge import vector_db

def evaluate_math_expression(expression: str) -> str:
    # Evaluates a mathematical expression string.
    # Used strictly for calculations.

    sys_logger.info(f"Tool Call: evaluate_math_expression -> {expression}")

    try:
        result = eval(expression)
        sys_logger.info(f"Tool Success: {expression} = {result}")
        return f"Calculation Result: {expression} = {result}"
    except Exception as e:
        sys_logger.error(f"Tool Error evaluating math: {e}")
        return f"Error evaluating mathematical expression: {str(e)}"

def real_web_search(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        if not results:
            return f"No results found on the web for '{query}'."

        formatted = []

        for r in results:
            title = r.get("title", "No title")
            body = r.get("body", "No description")
            href = r.get("href", "")

            formatted.append(
                f"Title: {title}\n"
                f"Description: {body}\n"
                f"Link: {href}\n"
            )

        return "\n".join(formatted)

    except Exception as e:
        return f"Web search failed: {str(e)}"
    
# Lightweight, highly accurate Cross-Encoder for reranking
# ms-marco is specifically trained for Question-Answering tasks
sys_logger.info("Loading Cross-Encoder model...")
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def advanced_rag_search(query: str) -> str:
    """
    Executes a Two-Stage Retrieval pipeline: LanceDB Hybrid Search -> Cross-Encoder Reranking.
    Use this tool whenever you need to search the knowledge base for facts or documents.
    """
    sys_logger.info(f"Tool Call: advanced_rag_search -> '{query}'")
    
    try:
        # STAGE 1: High Recall Hybrid Search (LanceDB pulls top 15)
        # Because knowledge_base is configured with SearchType.hybrid, this does both vector & keyword search automatically.
        raw_results = vector_db.search(query, limit=15)
        
        if not raw_results:
            return "No relevant documents found in the knowledge base."

        # STAGE 2: High Precision Reranking (Cross-Encoder scores the top 15)
        pairs = [[query, doc.content] for doc in raw_results]
        scores = reranker.predict(pairs)
        
        # Sort the results by the highest cross-encoder score
        ranked_indices = np.argsort(scores)[::-1]
        
        # Extract the top 3 absolute best chunks
        top_3_docs = [raw_results[i] for i in ranked_indices[:3]]
        top_3_scores = [scores[i] for i in ranked_indices[:3]]
        
        # Format the output so the LLM is forced to cite its exact sources
        formatted_context = "RETRIEVED KNOWLEDGE BASE CONTEXT:\n\n"
        for idx, (doc, score) in enumerate(zip(top_3_docs, top_3_scores)):
            formatted_context += f"--- Source Chunk {idx + 1} (Relevance Score: {score:.2f}) ---\n"
            formatted_context += f"{doc.content}\n\n"
            
        sys_logger.info("Two-stage retrieval and reranking complete.")
        return formatted_context
        
    except Exception as e:
        sys_logger.error(f"Error in advanced_rag_search: {e}", exc_info=True)
        return f"System Error during retrieval: {str(e)}"