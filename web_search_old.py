import requests
from bs4 import BeautifulSoup


def search_web(query):
    url = "https://www.google.com/search"

    params = {
        "q": query,
        "num": 5
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for result in soup.select("a"):
        heading = result.select_one("h3")

        if heading:
            title = heading.get_text(strip=True)
            link = result.get("href")

            if link and link.startswith("http"):
                results.append({
                    "title": title,
                    "url": link
                })

    return results[:5]


if __name__ == "__main__":
    results = search_web("Python programming")

    print("🔎 Search results:")
    print()

    for result in results:
        print("Title:", result["title"])
        print("URL:", result["url"])
        print()
