from web_search import search_web


def handle_web(user_input, max_results=5):
    results = search_web(
        user_input,
        max_results=max_results
    )

    if not results:
        return "No web search results found."

    formatted_results = []

    for result in results:
        formatted_results.append(
            f"TITLE: {result['title']}\n"
            f"URL: {result['href']}\n"
            f"INFO: {result['body']}"
        )

    return "\n\n".join(formatted_results)


if __name__ == "__main__":
    result = handle_web(
        "Python latest version",
        max_results=3
    )

    print("🌐 Web Handler:")
    print(result)
