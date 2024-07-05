import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.majidalfuttaim.com/en/investor-relations/financial-summary#FinancialStatements"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

pdf_links = soup.find_all('a', href=lambda href: href and (href.lower().endswith('.pdf') or '.pdf?' in href.lower()))
pdf_data_sources = [link['href'] for link in pdf_links]

with open('pdf_urls.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['PDF URL'])
    for href in pdf_data_sources:
        writer.writerow([href])
        print("PDF Source:", href)
print(len(pdf_data_sources))