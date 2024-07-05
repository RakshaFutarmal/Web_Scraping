import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.dewa.gov.ae/en/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

menu_urls = []

main_menu = soup.find(class_='m12-bar__wrapper')

def extract_menu_urls(menu_element):
    main_menu_items = menu_element.find_all('li', recursive=False)
    for item in main_menu_items:
        main_menu_link = item.find('a').get('href') if item.find('a') else None

        sub_menu_urls = []

        sub_menu_items = item.find_all('li', recursive=True)
        for sub_item in sub_menu_items:
            sub_menu_link = sub_item.find('a').get('href') if sub_item.find('a') else None
            if sub_menu_link:
                sub_menu_urls.append(sub_menu_link)

        menu_urls.append((main_menu_link, sub_menu_urls))

extract_menu_urls(main_menu)

csv_file = 'menu_urls.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Main Menu URL', 'Sub Menu URL'])

    for main_url, sub_urls in menu_urls:
        writer.writerow([main_url, ''])

        for sub_url in sub_urls:
            writer.writerow(['', sub_url])

print(f"Menu URLs scraped and saved to '{csv_file}'")
