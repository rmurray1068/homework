from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass


@dataclass
class Headline:
    date: str
    txt: str
    score: int


########Scrape set up area######

# def get_data()-> BeautifulSoup:
#     resp = requests.get("Bio website url goes here")
#     return BeautifulSoup(resp.content, "html.parser")

# test = get_data()

# table = test.find_all('HEADLINE TAG')

############Build the headline Objects################

head_line_list = [Headline("today", "Great news for bio company as FDA approves their drug trial", 0),
                  Headline("tomorrow", "bad news for bio company as FDA denies their drug trial after it fails", 0),
                  Headline("yeserday", "trial fails and investors worry, but good news in the future", 0)
                  ]

#################################

#list of pos/neg words

negative_words = ["Great", "approves", "good"]
positive_words = ["bad", "denies", "fails"]


#######Scoring Section#######

"""

Here we will run some loops through both lists. There will then be a positive or negative score


"""


def scoreHeadline(h1List: list):
    '''takes in a list of headline objects and scores them'''
    new_list = []
    for hl in h1List:
        sentiment = 0
        for word in positive_words:
            for headlineWord in hl.txt.split():
                if headlineWord == word:
                    sentiment += 1
        for word in negative_words:
            for headLineWord in hl.txt.split():
                if headLineWord == word:
                    sentiment -= 1
        new_list.append(Headline(hl.date, hl.txt, sentiment))
    return new_list
         

scoreHeadline(head_line_list)
