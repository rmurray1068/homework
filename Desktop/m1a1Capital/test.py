import csv
from textblob import TextBlob
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import datetime
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# train a custom sentiment classifier using your own labeled dataset
training_data = [
("New treatment for cancer shows promising results", 'pos'),
("Controversial study raises concerns about vaccine safety", 'neg'),
("Researchers identify new target for Alzheimer's therapy",'neu'),
("FDA approves new drug for rare genetic disorder", 'pos'),
("Clinical trial shows mixed results for new heart disease treatment", 'neu'),
("Study finds potential link between air pollution and cancer risk", 'neg'),
("New research suggests promising approach for treating diabetes", 'pos'),
("Scientists develop new method for detecting early-stage cancer", 'pos'),
("Controversial drug trial sparks debate over ethical issues", 'neg'),
("New gene therapy approach shows potential for treating rare disease", 'pos')
]
custom_analyzer = NaiveBayesAnalyzer(training_data)

# use the custom analyzer to analyze sentiment



@dataclass
class Headline:
    date: str
    txt: str
    score: str


def get_sentiment(text):
    analysis = TextBlob(text, analyzer=custom_analyzer)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def get_data() -> BeautifulSoup:
    resp = requests.get("https://www.biopharmadive.com/topic/clinical-trials/")
    return BeautifulSoup(resp.content, "html.parser")


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
            sentiment = get_sentiment(text)
            headline = Headline(today, text, sentiment)
            writer.writerow([headline.date, headline.txt, headline.score])


data = get_data()
gatherHeadlines(data, "headlines.csv")
