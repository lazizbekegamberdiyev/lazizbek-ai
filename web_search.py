from ddgs import DDGS


def search_web(query, max_results=5):
    results = DDGS().text(
        query,
        max_results=max_results
    )

    return results


if __name__ == "__main__":
    results = search_web(
        "ETH Zurich Masters admission requirements",
        3
    )

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(result['href'])
        print(result['body'])
