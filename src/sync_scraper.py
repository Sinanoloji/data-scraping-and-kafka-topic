from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

start_time = time.time()
url = "https://scrapeme.live/shop/"

#URL of Subdivision Pages
pages = []

#Data Groups
names = []
prices = []
descriptions = []
stocks = []

# Geting subdivision pages
def geting_pages(main_url):
    scrape = requests.get(main_url)
    soup = BeautifulSoup(scrape.text,"html.parser")
    hrefs = soup.findAll("a",attrs={"class":"woocommerce-LoopProduct-link woocommerce-loop-product__link"})
    for href in hrefs:
        pages.append(href.get("href"))

def scrape(page_num):
    data_scrape = requests.get(pages[page_num])
    data_soup = BeautifulSoup(data_scrape.text,"html.parser")
    name = data_soup.find("h1",attrs={"class":"product_title entry-title"})
    description = data_soup.find("div",attrs={"class":"woocommerce-product-details__short-description"})
    price = data_soup.find("p",attrs={"class":"price"})
    stock = data_soup.find("p",attrs={"class":"stock in-stock"})
    names.append(name.text)
    descriptions.append(description.text)
    prices.append(price.text)
    stocks.append(stock.text)


def main():
#Find data groups and save lists
    geting_pages(url)
    for i in range(len(pages)):
        scrape(i)
        
    # Save CSV file
    df = pd.DataFrame({"name":names,"price":prices,"description":descriptions,"stock":stocks})
    df.to_csv("data/pokemon.csv",index=False)

    # Convert to JSON file
    """ csv = pd.read_csv("pokemon.csv")
    csv.replace('(^\s+|\s+$)', '', regex=True, inplace=True)
    csv.to_json("time.json",orient="records",lines=False,indent=4,force_ascii=False) """

    time_difference = time.time() - start_time
    print(f'Scraping time: %.2f seconds.' % time_difference)

if __name__ == "__main__":
    main()





