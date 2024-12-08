import time
from pprint import pprint
import httpx
from parsel import Selector

ORIGIN_URL = "https://www.azattyk.org"
MAIN_URL = "https://www.azattyk.org/news"
NUM_URL = "https://www.azattyk.org/news?p="

def get_page(url):
    response = httpx.get(url)
    html = Selector(text=response.text)
    return html


def get_links(html: Selector):
    links = html.css("div.media-block a::attr(href)").getall()
    result_links = []
    c = 0
    for i in range(len(links) -1):
        if c == 0:
            result_links.append(ORIGIN_URL + links[i])
            c = 1
        else:
            c =0
    return result_links


def get_title(html: Selector):
    title = [text.strip() for text in html.css("div.media-block__content.media-block__content--h ::text")
    .getall() if text.strip()]
    result_title = []
    c = 1
    for i in range(len(title) -1):
        if c == 0:
            result_title.append(title[i])
            c = 1
        else:
            c =0
    return result_title

def get_text(link):
    page = get_page(link)
    text = [text.strip() for text in page.css("p::text").getall() if text.strip()]
    return text

def get_all_data(link):
    page = get_page(link)
    titles = get_title(page)
    links = get_links(page)
    texts = []
    for i in links:
        texts.append(get_text(i))
    results = []
    print(len(links), links)
    print(len(titles), titles)
    print(len(texts), texts)
    # for i in range(len(links) -1):
        # new_data={}
        # new_data['link'] = links[i]
    #     new_data['title'] = titles[i]
    #     new_data['text'] = texts[i]
    #     results.append(new_data)
    return links



all_news = []
for i in range(1, 10):
    once_result = get_all_data(NUM_URL + f"{i}")
    print(i)
    # all_news.extend(once_result)


# pprint(all_news)