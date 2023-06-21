from bs4 import BeautifulSoup
import requests
import pandas as pd
import asyncio
import aiohttp
import time

urls = []
cars = []
results = []

true_car = requests.get("https://www.truecar.com/used-cars-for-sale/listings/?page=1").text

soup = BeautifulSoup(true_car, 'lxml')

start = time.time()

#carcom = requests.get

def get_total_pages(soup):

    new_page = soup.find_all('li', {'data-test' : 'paginationDirectionalItem'})
    print(len(new_page))
    next_page = new_page[1].find('a').get('href')

    total_page_numbers = ""

    for char in next_page:
        if char.isdigit():
            total_page_numbers = total_page_numbers + char

    total_page_numbers = int(total_page_numbers) 

    return total_page_numbers

#total_page_numbers = range(int(get_total_pages(soup) / 37))

def get_tasks(session):
    tasks = []
    for page in range(1, int((get_total_pages(soup) / 37))):
        tasks.append(session.get(f"https://www.truecar.com/used-cars-for-sale/listings/?page={page}", ssl=False))
    print("done",len(tasks))
    return tasks

async def get_urls(loop):
    #timeout = aiohttp.ClientTimeout(total=100)
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = get_tasks(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            results.append(await response.text())

loop = asyncio.get_event_loop()
loop.run_until_complete(get_urls(loop))
loop.close()

for current_page in results:

    #print('getting page {page_number}')
    #true_car = requests.get(f"https://www.truecar.com/used-cars-for-sale/listings/?page={page_number}").text

    soup = BeautifulSoup(current_page, 'lxml')

    true_car_page = soup.find_all('div', {'data-test' : 'cardContent'})

    links = soup.find_all('a', {'data-test' : 'cardContent'})
    #print(links)

    #print(test[3].find('div', {}).get_text())
    for car in range(len(true_car_page)):
        name = true_car_page[car].find('span', {'class':'truncate'}).get_text()
        year = true_car_page[car].find('span', {'class' : 'vehicle-card-year text-xs'}).get_text()
        price = true_car_page[car].find('div', {'data-test' : 'vehicleCardPricingBlockPrice'}).get_text()
        if price.count('$') > 1:
            
            price = price[price.index('$',1):]

        link = true_car_page[car].find('a').get('href')
        car = {
            "Name": name,
            "Year": year,
            "Price": price,
            "Link": link
        }
        cars.append(car)


end = time.time()
ttime = end - start
        
df = pd.DataFrame(cars)

print(df)
print(ttime)
        #print(year, name, price, link)
    #print(len(test))
#df.to_excel('test.xlsx', index=False)
