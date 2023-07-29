import requests
from bs4 import BeautifulSoup
import json

def scrape_anime():
    products = []
    num_pages = 5

    for i in range(1, num_pages + 1):
        link = f'https://shikimori.me/animes/page/{i}/'
        page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
        
        if page.status_code != 200:
            print(f"Failed to fetch data from {link}. Status code: {page.status_code}")
            continue
        
        soup = BeautifulSoup(page.text, 'lxml')

        titles_raw = soup.find_all('span', class_='name-en')

        titles = [title.get_text(strip=True) for title in titles_raw]

        for title in titles:
            products.append({'title': title})

    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print("Scraping and JSON dumping completed.")
