import requests
from bs4 import BeautifulSoup
import urllib.parse

def fetch_links_with_query(query):
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve search results")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    links = []
    for item in soup.find_all('a'):
        href = item.get('href')
        if href and href.startswith('http'):
            links.append(href)

    links = links[3:]

    return links

if __name__ == "__main__":
    query = input("Enter your query: ")  
    links = fetch_links_with_query(query)

    print("\nLinks:")
    for link in links:
        print(link)
