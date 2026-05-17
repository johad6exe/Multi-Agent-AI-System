from duckduckgo_search import DDGS
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

def real_web_search(query: str) -> str:
    # Searches the web using DuckDuckGo to find real-time information.
    # Used when the user asks about current events, news, or general web facts.

    sys_logger.info(f"Tool Call: real_web_search -> '{query}'")
    
    try:
        # Initialize DuckDuckGo search and grab the top 3 results
        results = DDGS().text(query, max_results=3)
        
        if not results:
            sys_logger.warning(f"Tool Warning: No results found for '{query}'")
            return f"No results found on the web for '{query}'."

        # Format the raw JSON results into a clean string for the LLM to read
        formatted_results = "\n\n".join(
            [f"Title: {res['title']}\nSnippet: {res['body']}\nLink: {res['href']}" for res in results]
        )
        
        sys_logger.info("Tool Success: Web search completed and data retrieved.")
        
        return f"Real-Time Search Results for '{query}':\n\n{formatted_results}"
        
    except Exception as e:
        sys_logger.error(f"Tool Error during web search: {e}", exc_info=True)
        return f"Error performing web search: {str(e)}"