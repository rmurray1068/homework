import csv
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import datetime

@dataclass
class Headline:
    date: str
    txt: str
    score: str


#next pages take this url format https://www.biopharmadive.com/topic/clinical-trials/?page=3

def get_data() -> BeautifulSoup:
    resp = requests.get("https://www.biopharmadive.com/topic/clinical-trials/")
    return BeautifulSoup(resp.content, "html.parser")

data = get_data()

def gatherHeadlines(soup: BeautifulSoup, filename: str):
    today = datetime.datetime.now().strftime('%B %d, %Y')
    link_text = []
    for link in soup.find_all('a'):
        if len(link.text.strip().split()) > 4:
            link_text.append(link.text.strip())

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Headline', 'Score'])

        for text in link_text:
            score = 0
            headline = Headline(today, text, score)
            writer.writerow([headline.date, headline.txt, headline.score])


gatherHeadlines(data, "headlines.csv")
