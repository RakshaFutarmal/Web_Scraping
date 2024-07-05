
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
import csv
import threading

url_to_scrape = "https://www.regeny.ae/"

parsed_url = urlparse(url_to_scrape)
base_domain = parsed_url.netloc

visited_urls = set()

lock = threading.Lock()

with open('chargemap.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['URL', 'Title', 'Text'])

    def is_same_domain(url, base_domain):
        parsed_extracted_url = urlparse(url)
        return parsed_extracted_url.netloc == base_domain

    def is_unnecessary_url(url):
        unnecessary_patterns = ['login', 'signup', 'register', 'terms', 'privacy']
        return any(pattern in url for pattern in unnecessary_patterns)

    def crawl(url):
        if url in visited_urls:
            return

        with lock:
            visited_urls.add(url)

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

            response = requests.get(url,headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            for tag in soup.find_all(['header', 'footer']):
                tag.decompose()

            title = soup.title.string if soup.title else 'No title'
            text = soup.get_text(separator=' ', strip=True)
            print(f"Crawling URL: {url}")
            print(f"Title: {title}")

            with lock:
                writer.writerow([url, title, text])

            links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]

            threads = []
            for link in links:
                if is_same_domain(link, base_domain) and not is_unnecessary_url(link):
                    thread = threading.Thread(target=crawl, args=(link,))
                    threads.append(thread)
                    thread.start()

            for thread in threads:
                thread.join()

        except requests.RequestException as e:
            print(f"Failed to crawl {url}: {e}")

    crawl(url_to_scrape)
