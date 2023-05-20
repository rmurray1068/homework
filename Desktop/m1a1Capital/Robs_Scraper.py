import csv
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import datetime
from urllib.parse import urljoin

@dataclass
class Headline:
    date: str
    txt: str
    score: str

def get_data(url: str) -> BeautifulSoup:
    resp = requests.get(url)
    return BeautifulSoup(resp.content, "html.parser")

base_url = "https://www.biopharmadive.com/topic/clinical-trials/"
num_pages = 20  # Specify the number of subsequent pages to scrape

def gatherHeadlines(soup: BeautifulSoup, filename: str):
    today = datetime.datetime.now().strftime('%B %d, %Y')
    divs = soup.find_all('div', class_='medium-8 columns')
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(['Date', 'Headline', 'Score'])

        for div in divs:
            headline = div.find('h3', class_='feed__title')
            if headline:
                text = headline.find('a').text.strip()
                date_span = div.find_all('span', class_='secondary-label')
                if len(date_span) >= 2:
                    date = date_span[1].text.strip()
                    score = 0
                    headline_obj = Headline(date, text, score)
                    writer.writerow([headline_obj.date, headline_obj.txt, headline_obj.score])

# Scrape the first page
first_page_url = base_url
data = get_data(first_page_url)
gatherHeadlines(data, "headlines.csv")

# Scrape subsequent pages
for page in range(2, num_pages + 1):
    next_page_url = urljoin(base_url, f"?page={page}")
    data = get_data(next_page_url)
    gatherHeadlines(data, "headlines.csv")
