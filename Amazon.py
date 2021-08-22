from selenium import webdriver
import lxml
from bs4 import BeautifulSoup
import csv



def get_html(query, page):
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.maximize_window()
    query = query.replace(" ", "+")
    for i in range(page+1):
        url = f'https://www.amazon.in/s?k={query}&page={i}&qid=1629573111&ref=sr_pg_{i}'
        driver.get(url=url)
        html = driver.page_source
    # driver.find_element_by_id('twotabsearchtextbox').send_keys(query)
    # driver.find_element_by_id('nav-search-submit-button').click()
        soup = BeautifulSoup(html, 'lxml')
        cards = soup.findAll('div', {'data-asin': True, 'data-component-type': 's-search-result'})
        for card in cards:
            get_details(card)


def csv_file(item_image, title, href, price, rating, Delivery):
    with open(f"{query}.csv", 'a', newline='', encoding="utf-8") as f:
        fields = ["Image","Title", "Price", "Rating", "Delivery", "Link"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow({"Image":item_image, "Title": title, "Price": price, "Rating": rating, "Delivery": Delivery, "Link": href })
    f.close()


def get_details(card):
    item_list = []

    try:
        h2 = card.h2
        item_img = card.img
    except:
        title = ""
        href = ""
        item_image = ""
        item_list.append(title)
        item_list.append(href)
        item_list.append (item_image)
    else:
        title = h2.text
        href = "https://www.amazon.in/" + h2.a.get('href')
        item_image = item_img.get('src')

        item_list.append(title)
        item_list.append(href)
        item_list.append (item_image)


    try:
        price = card.find('span', class_='a-price-whole').text
        rating = card.find('span', class_='a-icon-alt').text
        rating = rating.split(" ")[0]
        Delivery = card.find('span', class_='a-text-bold').text

    except:
        price = "Not Available"
        rating = "Not Available"
        Delivery = "Not Available"
        item_list.append(price)
        item_list.append(rating)
        item_list.append(Delivery)

    else:
        price_item = price
        rating = rating
        Delivery = Delivery
        item_list.append(price)
        item_list.append(rating)
        item_list.append(Delivery)

    csv_file(item_image, title, href, price, rating, Delivery)

print("Welcome To Amazon Scrapper")

query = input("Name of product you want to search for ?\n")
page = int(input("On how many pages you want me to look?\n"))
with open(f"{query}.csv", 'a', newline = '', encoding = "utf-8") as f:
    fields = ["Image", "Title", "Price", "Rating", "Delivery", "Link"]
    writer = csv.DictWriter(f, fieldnames = fields)
    writer.writeheader()
f.close()
get_html(query, page)
print("Process Completed")


