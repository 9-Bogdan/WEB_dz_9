import re
import requests
from bs4 import BeautifulSoup
from json import dump


def parse_quotes():
    base_url = "http://quotes.toscrape.com/page/"
    page = 1
    finish_list = []
    while True:
        html = requests.get(base_url + f"{page}/")
        if html.status_code == 200:
            if not "No quotes found!" in html.text:
                soup = BeautifulSoup(html.text, "html.parser")
                quotes = soup.select("div[class=quote] span[class=text]")
                authors = soup.select(
                    "div[class=quote] span small[class = author]")
                tags = soup.find_all('div', class_='tags')
                for i in range(0, len(quotes)):
                    tagsforquote = tags[i].find_all('a', class_='tag')
                    tags_list = []
                    for tagforquote in tagsforquote:
                        tags_list.append(tagforquote.text)
                    quote_dict = {"tags": tags_list,
                                  "author": authors[i].text,
                                  "quote": quotes[i].text}
                    finish_list.append(quote_dict)
                page += 1
            else:
                break
    dump_quotes(finish_list)


def parse_authors_links():
    page = 1
    base_url = "http://quotes.toscrape.com/page"
    links_author = []
    while True:
        html = requests.get(base_url + f"/{page}/")
        if html.status_code == 200:
            if not "No quotes found!" in html.text:
                soup = BeautifulSoup(html.text, "html.parser")
                authors = soup.select("div[class=quote] span a")
                for author in authors:
                    links_author.append(base_url.removesuffix(
                        "/page") + str(author["href"]))
                page += 1
            else:
                break
    parse_authors(links_author)


def parse_authors(links_author: list):
    authors_list = []
    for link in links_author:
        html = requests.get(link)
        soup = BeautifulSoup(html.text, "html.parser")
        author_fullname = soup.find('div', class_="author-details").find('h3')
        born_date = soup.find(
            'div', class_="author-details").find('p').find('span', class_="author-born-date")
        born_location = soup.find(
            'div', class_="author-details").find('p').find('span', class_="author-born-location")
        description = soup.find(
            'div', class_="author-details").find('div', class_="author-description")
        # print(author_fullname.text)
        # print(born_date.text)
        # print(born_location.text)
        # print(description.text.strip())
        author_dict = {"name": author_fullname.text,
                       "born_date": born_date.text,
                       "born_location": born_location.text,
                       "description": description.text.strip()}
        if not author_dict in authors_list:
            authors_list.append(author_dict)
    dump_authors(authors_list)
    return authors_list


def dump_authors(authors):
    with open("authors.json", "w", encoding="utf-8") as fd:
        dump(authors, fd, indent=2, ensure_ascii=False)


def dump_quotes(quotes: list):
    with open("quotes.json", "w", encoding="utf-8") as fd:
        dump(quotes, fd, indent=2, ensure_ascii=False)


parse_quotes()
parse_authors_links()
