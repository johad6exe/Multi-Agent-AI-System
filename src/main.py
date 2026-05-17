from src.tools import evaluate_math_expression, real_web_search

def main():
    # Example usage of the tools
    print("what tool do you want to use?")
    choice = input("Enter 'math' for math evaluation or 'search' for web search: ").strip().lower()

    if choice == 'math':
        expression = input("Enter a mathematical expression to evaluate (e.g., '2 + 2 * 3'): ")
        math_result = evaluate_math_expression(expression)
        print(math_result)
    elif choice == 'search':
        query = input("Enter a search query: ")
        search_result = real_web_search(query)
        print(search_result)

if __name__ == "__main__":
    main()