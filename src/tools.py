from ddgs import DDGS
import numpy as np
from sentence_transformers import CrossEncoder
from src.knowledge import knowledge_base
from src.logger import sys_logger

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
    
    # Executes a two-stage retrieve-and-rerank pipeline.
    # Use this tool whenever you need to search the knowledge base for facts or documents.

    sys_logger.info(f"Tool Call: advanced_rag_search -> '{query}'")
    
    try:
        # STAGE 1: High Recall Retrieval (Bi-Encoder via DuckDB)
        # Fetch a wide net of 15 documents 
        raw_results = knowledge_base.search(query, num_documents=15)
        
        if not raw_results:
            return "No relevant documents found in the knowledge base."

        # STAGE 2: High Precision Reranking (Cross-Encoder)
        # Pair the user query with every retrieved chunk for deep semantic scoring
        pairs = [[query, doc.content] for doc in raw_results]
        scores = reranker.predict(pairs)
        
        # Sort the results by the cross-encoder score in descending order
        # We use numpy argsort to get the indices of the highest scores
        ranked_indices = np.argsort(scores)[::-1]
        
        # Extract the top 3 most semantically relevant chunks
        top_3_docs = [raw_results[i] for i in ranked_indices[:3]]
        top_3_scores = [scores[i] for i in ranked_indices[:3]]
        
        # Format the output explicitly so the LLM must cite its sources
        formatted_context = "RETRIEVED KNOWLEDGE BASE CONTEXT:\n\n"
        for idx, (doc, score) in enumerate(zip(top_3_docs, top_3_scores)):
            formatted_context += f"--- Source Chunk {idx + 1} (Relevance Score: {score:.2f}) ---\n"
            formatted_context += f"{doc.content}\n\n"
            
        sys_logger.info("Two-stage retrieval and reranking complete.")
        return formatted_context
        
    except Exception as e:
        sys_logger.error(f"Error in advanced_rag_search: {e}", exc_info=True)
        return f"System Error during retrieval: {str(e)}"