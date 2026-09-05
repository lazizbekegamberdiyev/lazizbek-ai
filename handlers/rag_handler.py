from rag import search_documents


def handle_rag(user_input, n_results=3):
    results = search_documents(
        user_input,
        n_results=n_results
    )

    if not results:
        return "The uploaded documents do not contain enough relevant information."

    formatted_results = []

    for result in results:
        formatted_results.append(
            f"SOURCE: {result['source']}\n"
            f"PAGE: {result['page']}\n"
            f"CONTENT: {result['text']}"
        )

    return "\n\n".join(formatted_results)


if __name__ == "__main__":
    result = handle_rag(
        "What is panel data?"
    )

    print("📚 RAG Handler:")
    print(result)
