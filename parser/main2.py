import time
from pprint import pprint
import httpx
from parsel import Selector
from time import sleep

MAIN_URL = "https://sputnik.kg/news/"
ORIGINAL_URL = "https://sputnik.kg"
NEXT_PAGE_URL = "https://sputnik.kg/services/news/more.html?id=1090615207&date=20241205T094323&onedayonly=1&articlemask=lenta"

def get_page(url):
    response = httpx.get(url)
    html = Selector(text=response.text)
    return html


def get_link_next_page(html):
    new_link = html.css("div.list-items-loaded::attr(data-next-url)").get()
    return ORIGINAL_URL + new_link

def get_link_next_page_1(html):
    new_link = html.css("div.list__more::attr(data-url)").get()
    return ORIGINAL_URL + new_link

def get_detail_text(link):
    page = get_page(link)
    text = page.css("div.article__text::text").getall()
    return "".join(text)

def get_all_data_pages(link):
    html = get_page(link)
    houses = html.css("div.list__item")
    news_list = []
    for house in houses:
        link = ORIGINAL_URL + house.css("div.list__item a::attr(href)").get()
        title = house.css("div.list__item a::attr(title)").get()
        text = get_detail_text(link)
        news_data = {}
        news_data['title'], news_data['text'], news_data['link'] = title, text, link
        news_list.append(news_data)
    return news_list

def get_all_data_1(link):
    html = get_page(link)
    houses = html.css("div.list__item")
    news_list = []
    for house in houses:
        link = house.css("div.list__item a::attr(href)").get()
        title = house.css("div.list__item a::attr(title)").get()
        text = get_detail_text(link)
        news_data = {}
        news_data['title'], news_data['text'], news_data['link'] = title, text, link
        news_list.append(news_data)
    return news_list


def run(link):
    results = []
    results.extend(get_all_data_1(link))
    print("parsed")
    page = get_page(link)
    link = get_link_next_page_1(page)
    time.sleep(5)
    for i in range(6):
        results.extend(get_all_data_pages(link))
        print("parsed")
        page = get_page(link)
        link = get_link_next_page(page)
        time.sleep(5)
    for i in results:
        print(i)

    return results



if __name__ == "__main__":
    results = run(MAIN_URL)
    # pprint(results)import time
from pprint import pprint
import httpx
from parsel import Selector
from time import sleep

MAIN_URL = "https://sputnik.kg/news/"
ORIGINAL_URL = "https://sputnik.kg"
NEXT_PAGE_URL = "https://sputnik.kg/services/news/more.html?id=1090615207&date=20241205T094323&onedayonly=1&articlemask=lenta"

def get_page(url):
    response = httpx.get(url)
    html = Selector(text=response.text)
    return html


def get_link_next_page(html):
    new_link = html.css("div.list-items-loaded::attr(data-next-url)").get()
    return ORIGINAL_URL + new_link

def get_link_next_page_1(html):
    new_link = html.css("div.list__more::attr(data-url)").get()
    return ORIGINAL_URL + new_link

def get_detail_text(link):
    page = get_page(link)
    text = page.css("div.article__text::text").getall()
    return "".join(text)

def get_all_data_pages(link):
    html = get_page(link)
    houses = html.css("div.list__item")
    news_list = []
    for house in houses:
        link = ORIGINAL_URL + house.css("div.list__item a::attr(href)").get()
        title = house.css("div.list__item a::attr(title)").get()
        text = get_detail_text(link)
        news_data = {}
        news_data['title'], news_data['text'], news_data['link'] = title, text, link
        news_list.append(news_data)
    return news_list

def get_all_data_1(link):
    html = get_page(link)
    houses = html.css("div.list__item")
    news_list = []
    for house in houses:
        link = house.css("div.list__item a::attr(href)").get()
        title = house.css("div.list__item a::attr(title)").get()
        text = get_detail_text(link)
        news_data = {}
        news_data['title'], news_data['text'], news_data['link'] = title, text, link
        news_list.append(news_data)
    return news_list


def run(link):
    results = []
    results.extend(get_all_data_1(link))
    print("parsed")
    page = get_page(link)
    link = get_link_next_page_1(page)
    time.sleep(5)
    for i in range(6):
        results.extend(get_all_data_pages(link))
        print("parsed")
        page = get_page(link)
        link = get_link_next_page(page)
        time.sleep(5)
    for i in results:
        print(i)

    return results



if __name__ == "__main__":
    results = run(MAIN_URL)
    # pprint(results)