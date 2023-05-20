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
    today = datetime.datetime.now().strftime('%B %d, %Y')#fix this to grab date
    link_text = []
    for link in soup.find_all('a'):
        if len(link.text.strip().split()) > 4:
            link_text.append(link.text.strip())

    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # Write header only if file is empty
            writer.writerow(['Date', 'Headline', 'Score'])

        for text in link_text:
            score = 0
            headline = Headline(today, text, score)
            writer.writerow([headline.date, headline.txt, headline.score])

# Scrape the first page
first_page_url = base_url
data = get_data(first_page_url)
gatherHeadlines(data, "headlines.csv")

# Scrape subsequent pages
for page in range(2, num_pages + 1):
    next_page_url = urljoin(base_url, f"?page={page}")
    data = get_data(next_page_url)
    gatherHeadlines(data, "headlines.csv")