from ddgs import DDGS
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