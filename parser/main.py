from pprint import pprint
import httpx
from parsel import Selector

MAIN_URL = "https://www.house.kg/snyat"
ORGINAL_URL = "https://www.house.kg"
url = 'https://www.best-tyres.ru/'

def get_page(url):
    response = httpx.get(url)
    html = Selector(text=response.text)
    return html

def get_title(html: Selector):
    title = html.css("title::text").get()
    print(title)

def get_cars_links(html: Selector):
    cars_links = html.css("div.left-image a::attr(href)").getall()
    # pprint(cars)
    # cars = [f"{ORGINAL_URL}{car}" for car in cars]
    cars = list(map(lambda car: f"{ORGINAL_URL}{car}", cars_links))
    pprint(cars)

def clean_text(text: str):
    if text is None:
        return ""
    text = " ".join(text.split())
    return text.strip().replace("\t", "").replace("\n", "")

def price_to_int(price:str):
    result_price = ''
    for i in price:
        if i.isdigit():
            result_price+=i
    return int(result_price)
def get_house_data(html: Selector):
    houses = html.css("div.main-wrapper")
    houses_list = []
    for house in houses:
        house_data = {}
        house_data["title"] = clean_text(house.css("p.title a::text").get())
        house_data["price"] = price_to_int(clean_text(house.css("div.price::text").get()))
        house_data["som_price"] = price_to_int(clean_text(house.css("div.price-addition::text").get()))
        house_data["house_description"] = clean_text(house.css("div.description::text").get())
        house_data['address'] = clean_text(house.css("div.address::text").getall()[1])
        houses_list.append(house_data)
    return houses_list

def get_houses():
    houses = []
    for page in range(1, 6):
        url = f"{MAIN_URL}?page={page}"
        html = get_page(url)
        houses.extend(get_house_data(html))
    # return get_cars_links(html)
    # pprint(cars)
    return houses
    # print("Lenght", len(houses))

if __name__ == '__main__':
    page = get_page(MAIN_URL)
    houses = get_houses()
    print(houses)
    print('дома добавлены')