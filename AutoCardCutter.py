# required pip installs: requests, beautifulsoup4,

import requests
from googlesearch import search
from bs4 import BeautifulSoup

query = input("Enter a search term: ") + " cnn"
numb = int(input("Enter # of desired cards: "))

searches = search(query, tld="com", num=numb, stop=numb, pause=2)

articles = []
counter = 0


class Article:
    def __init__(self, url, author, date, title, text):
        self.url = url
        self.author = author
        self.date = date
        self.title = title
        self.text = text


for search in searches:
    page = requests.get(search)
    soup = BeautifulSoup(page.content, "html.parser")
    textResults = soup.find_all(class_="zn-body__paragraph")

    if len(textResults) > 0:
        text = ""
        for result in textResults:
            text += result.text + " "
        try:
            title = soup.find(class_="pg-headline").text
            date = soup.find(class_="update-time").text
            index = date.index(",") + 2
            date = date[index:len(date)-1]
            author = soup.find(class_="metadata__byline__author").find("a").text

            articles.append(Article(search, author, date, title, text))
            counter += 1
        finally:
            continue

f = open("cards.txt", "w")
f.write("")
f.close()

f = open("cards.txt", "a")
try:
    for article in articles:
        indexA = article.author.index(" ") + 1
        indexD = article.date.index(", 20") + 4
        f.write(article.title + "\n"
                + article.author[indexA:len(article.author)] + " " + article.date[indexD:len(article.date)] + " (" + article.author + ", " + article.date + ", " + article.title + ", CNN News, From " + article.url + ", VP)\n"
                + article.text + "\n\n")
finally:
    f.close()


print("\nTASK FINISHED: I was able to cut " + str(counter) + " card(s)")
