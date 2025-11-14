import requests
from bs4 import BeautifulSoup
import csv
import json
import time
from urllib.parse import urljoin, urlparse
import os


class WebScraper:
    def __init__(self, base_url: str, delay: float = 1.0):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_page(self, url: str) -> BeautifulSoup:
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_links(self, soup: BeautifulSoup, css_selector: str) -> list:
        links = []
        for link in soup.select(css_selector):
            href = link.get('href')
            if href:
                full_url = urljoin(self.base_url, href)
                links.append({
                    'text': link.get_text(strip=True),
                    'url': full_url
                })
        return links

    def scrape_text(self, soup: BeautifulSoup, css_selector: str) -> list:
        elements = soup.select(css_selector)
        return [elem.get_text(strip=True) for elem in elements]

    def scrape_table(self, soup: BeautifulSoup, table_selector: str) -> list:
        table = soup.select_one(table_selector)
        if not table:
            return []

        rows = []
        headers = []

        header_cells = table.select(
            'thead th, tr:first-child th, tr:first-child td')
        if header_cells:
            headers = [cell.get_text(strip=True) for cell in header_cells]

        for row in table.select('tr'):
            cells = row.select('td, th')
            if cells:
                row_data = [cell.get_text(strip=True) for cell in cells]
                if headers and len(row_data) == len(headers):
                    rows.append(dict(zip(headers, row_data)))
                else:
                    rows.append(row_data)

        return rows

    def save_to_csv(self, data: list, filename: str):
        if not data:
            print("No data to save")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            if isinstance(data[0], dict):
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            else:
                writer = csv.writer(csvfile)
                writer.writerows(data)

        print(f"Data saved to {filename}")

    def save_to_json(self, data: list, filename: str):
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")

    def scrape_multiple_pages(self, page_urls: list, scrape_func):
        all_data = []
        for url in page_urls:
            print(f"Scraping: {url}")
            soup = self.get_page(url)
            if soup:
                data = scrape_func(soup)
                all_data.extend(data)
            time.sleep(self.delay)
        return all_data


def scrape_news_example():
    scraper = WebScraper("https://news.ycombinator.com")

    soup = scraper.get_page(scraper.base_url)
    if not soup:
        return

    print("Scraping Hacker News headlines...")
    headlines = scraper.scrape_links(soup, 'span.titleline > a')

    for i, headline in enumerate(headlines[:10], 1):
        print(f"{i}. {headline['text']}")
        print(f"   URL: {headline['url']}")
        print()

    scraper.save_to_json(headlines, 'hacker_news_headlines.json')


def scrape_quotes_example():
    scraper = WebScraper("http://quotes.toscrape.com")

    all_quotes = []
    page = 1

    while True:
        url = f"{scraper.base_url}/page/{page}/"
        print(f"Scraping page {page}: {url}")

        soup = scraper.get_page(url)
        if not soup or "No quotes found!" in soup.get_text():
            break

        quotes = []
        quote_elements = soup.select('div.quote')

        for quote_elem in quote_elements:
            text = quote_elem.select_one('span.text').get_text(strip=True)
            author = quote_elem.select_one('small.author').get_text(strip=True)
            tags = [tag.get_text(strip=True)
                    for tag in quote_elem.select('div.tags a.tag')]

            quotes.append({
                'text': text,
                'author': author,
                'tags': tags
            })

        all_quotes.extend(quotes)
        page += 1
        time.sleep(scraper.delay)

    scraper.save_to_json(all_quotes, 'quotes.json')
    scraper.save_to_csv(all_quotes, 'quotes.csv')
    print(f"Scraped {len(all_quotes)} quotes")


def scrape_table_example():
    scraper = WebScraper("https://www.w3schools.com/html/html_tables.asp")

    soup = scraper.get_page(scraper.base_url)
    if not soup:
        return

    print("Scraping HTML table example...")
    table_data = scraper.scrape_table(soup, 'table')

    if table_data:
        print("Table data:")
        for row in table_data[:5]:
            print(row)

        scraper.save_to_csv(table_data, 'table_data.csv')


def main():
    print("Web Scraping Examples")
    print("=" * 50)

    print("\n1. Scraping Hacker News headlines...")
    try:
        scrape_news_example()
    except Exception as e:
        print(f"Error scraping news: {e}")

    print("\n2. Scraping quotes...")
    try:
        scrape_quotes_example()
    except Exception as e:
        print(f"Error scraping quotes: {e}")

    print("\n3. Scraping table data...")
    try:
        scrape_table_example()
    except Exception as e:
        print(f"Error scraping table: {e}")

    print("\nScraping completed!")


if __name__ == "__main__":
    main()
