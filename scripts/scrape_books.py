"""
Web Scraper para https://books.toscrape.com/
Desenvolvido para o Tech Challenge - Pós-Tech | Fase 1 - Machine Learning Engineering

Este script coleta dados de todos os livros disponíveis no site e os salva no formato CSV.
Campos extraídos: título, preço, rating, disponibilidade, categoria, imagem

Execução:
    python scripts/scrape_books.py
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = BASE_URL + "catalogue/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Cria diretório para armazenar dados, se não existir
os.makedirs("data", exist_ok=True)


def get_soup(url):
    """Retorna o objeto BeautifulSoup de uma URL"""
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return None
    return BeautifulSoup(response.text, "html.parser")


def get_category_map():
    """Retorna um dicionário {url: categoria}"""
    soup = get_soup(BASE_URL)
    category_map = {}
    for cat in soup.select(".side_categories ul li ul li a"):
        name = cat.text.strip()
        link = BASE_URL + cat['href']
        category_map[link] = name
    return category_map


def extract_book_info(article, category_name):
    """Extrai os dados de um livro a partir do bloco HTML do artigo"""
    title = article.h3.a['title']
    link = article.h3.a['href'].replace('../../../', CATALOGUE_URL)

    # Preço com tratamento seguro
    price_element = article.select_one(".price_color")
    if price_element:
        price_text = price_element.text.strip().replace('£', '').replace(',', '.')
        try:
            price = float(price_text)
        except ValueError:
            price = 0.0
    else:
        price = 0.0

    rating = article.p['class'][1]
    availability = article.select_one(".instock.availability").text.strip()
    image_url = BASE_URL + article.find("img")["src"].replace("../", "")

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
        "category": category_name,
        "image_url": image_url,
        "link": link
    }



def scrape_category(category_url, category_name):
    """Raspagem de uma categoria completa com todas as páginas"""
    books = []
    page = 1
    while True:
        url = category_url.replace("index.html", f"page-{page}.html") if page > 1 else category_url
        soup = get_soup(url)
        if not soup:
            break
        articles = soup.select("article.product_pod")
        if not articles:
            break
        for article in articles:
            book = extract_book_info(article, category_name)
            books.append(book)
        page += 1
        time.sleep(0.5)
    return books


def main():
    print("📚 Iniciando scraping de livros...")
    all_books = []
    categories = get_category_map()
    for url, name in categories.items():
        print(f"🔎 Categoria: {name}")
        books = scrape_category(url, name)
        all_books.extend(books)
        print(f"✔ {len(books)} livros encontrados na categoria {name}")
    df = pd.DataFrame(all_books)
    df.to_csv("data/books.csv", index=False)
    print(f"\n✅ Scraping finalizado. Total de livros: {len(df)}")
    print("📁 Arquivo salvo em: data/books.csv")


if __name__ == "__main__":
    main()
