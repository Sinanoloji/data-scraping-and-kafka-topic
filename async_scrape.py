from bs4 import BeautifulSoup
import asyncio
import pandas as pd
import time
import aiohttp


pages = []

names = []
prices = []
descriptions = []
stocks = []


async def save_product(name,price,description,stock):
    df = pd.DataFrame({"name":name,"price":price,"description":description,"stock":stock})
    df.to_csv("pokemon.csv",index=False)

    # Convert to JSON file
    csv = pd.read_csv("time.csv")
    csv.replace('(^\s+|\s+$)', '', regex=True, inplace=True)
    csv.to_json("pokemon.json",orient="records",lines=False,indent=4,force_ascii=False)

async def scrape_pages(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.text()
            soup = BeautifulSoup(body,"html.parser")
            hrefs = soup.findAll("a",attrs={"class":"woocommerce-LoopProduct-link"})
            for href in hrefs:
                pages.append(href.get("href"))

async def scrape(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.text()
            soup = BeautifulSoup(body,"html.parser")
            name = soup.find("h1",attrs={"class":"product_title entry-title"})
            description = soup.find("div",attrs={"class":"woocommerce-product-details__short-description"})
            price = soup.find("p",attrs={"class":"price"})
            stock = soup.find("p",attrs={"class":"stock in-stock"})
            names.append(name.text)
            descriptions.append(description.text)
            prices.append(price.text)
            stocks.append(stock.text)
            await save_product(names,prices,descriptions,stocks)
    


async def main():

    start_time = time.time()
    url = "https://scrapeme.live/shop/"
    await scrape_pages(url)
    tasks = []
    for page in pages:
        task = asyncio.create_task(scrape(page))
        tasks.append(task)

    print("saving the output of extracted informaition")
    await asyncio.gather(*tasks)

    time_difference = time.time() - start_time
    print(f'Scraping time: %.2f seconds.' % time_difference)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())