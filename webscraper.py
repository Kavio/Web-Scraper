from bs4 import BeautifulSoup
import requests
import pandas as pd
import asyncio
import aiohttp
import tkinter
import time

cars = []

zip_code = input("Insert desired zipcode: ")
search_radius = input("Insert desired search radious from zipcode in miles: ")

start = time.time()

carcom = requests.get(f"https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=&maximum_distance={search_radius} \
                      &mileage_max=&monthly_payment=&page_size=100&sort=best_match_desc&stock_type=used&year_max=&year_min=&zip={zip_code}").text

true_car = requests.get(f"https://www.truecar.com/used-cars-for-sale/listings/location-{zip_code}/?page=1&searchRadius={search_radius}").text



def int_from_string(string):

    new_string = ""
    string = string[ :(string.index('&'))]

    for char in string:
        if char.isdigit():
            new_string = new_string + char
    return new_string

def scrape_truecar(true_car):
    
    results = []

    soup = BeautifulSoup(true_car, 'lxml')

    def get_total_pages(soup):

        new_page = soup.find_all('li', {'data-test' : 'paginationDirectionalItem'})
        
        next_page = new_page[1].find('a').get('href')

        total_page_numbers = int_from_string(next_page)

        total_page_numbers = int(total_page_numbers) 

        return total_page_numbers

    #total_page_numbers = range(int(get_total_pages(soup) / 37))

    def get_tasks(session):
        tasks = []
        for page in range(1, int((get_total_pages(soup) / 37))):
            tasks.append(session.get(f"https://www.truecar.com/used-cars-for-sale/listings/location-{zip_code}/?page={page}&searchRadius={search_radius}", ssl=False))
        print("done",len(tasks))
        return tasks

    async def get_urls(loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            tasks = get_tasks(session)
            responses = await asyncio.gather(*tasks)
            for response in responses:
                results.append(await response.text())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_urls(loop))
    

    for current_page in results:

        soup = BeautifulSoup(current_page, 'lxml')

        true_car_page = soup.find_all('div', {'data-test' : 'cardContent'})

        for car in range(len(true_car_page)):
            name = true_car_page[car].find('span', {'class':'truncate'}).get_text()
            year = true_car_page[car].find('span', {'class' : 'vehicle-card-year text-xs'}).get_text()
            '''price = true_car_page[car].find('div', {'data-test' : 'vehicleCardPricingBlockPrice'}).get_text()
            if price is None:
                price = ""
            if price.count('$') > 1:
                
                price = price[price.index('$',1):]
'''
            mileage = (true_car_page[car].find('div', {'data-test' : 'vehicleMileage'}).get_text()).strip("miles")
            car_location = true_car_page[car].find('div', {'class' :"vehicle-card-location mt-1 text-xs" }).get_text()
            number_of_accidents = true_car_page[22].find('div', {'data-test' :"vehicleCardCondition" }).get_text()
            if type(number_of_accidents[0]) is str:

                number_of_accidents = 0
            else:
                number_of_accidents = int_from_string(number_of_accidents)

            link = true_car_page[car].find('a').get('href')
            car = {
                "Name": name,
                "Year": year,
                "Mileage": mileage,
                "Location": car_location,
                "Number of Accidents": number_of_accidents,
               # "Price": price,
                "Link": link
            }
            cars.append(car)
    
    return  pd.DataFrame(cars)

def scrape_carscom(carcom):
    
    results = []

    def get_tasks(session):
        tasks = []
        for page in range(1, 2):
            tasks.append(session.get(f"https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=&maximum_distance={search_radius} \
                      &mileage_max=&monthly_payment=&page={page}&page_size=100&sort=best_match_desc&stock_type=used&year_max=&year_min=&zip={zip_code}", ssl=False))
        print("done",len(tasks))
        return tasks

    async def get_urls(loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            tasks = get_tasks(session)
            responses = await asyncio.gather(*tasks)
            for response in responses:
                results.append(await response.text())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_urls(loop))
    loop.close()

    for current_page in results:

        soup = BeautifulSoup(current_page, 'lxml')

        carcom_page = soup.find_all('div', {'class' : 'vehicle-card'})

        for car in range(len(carcom_page)):

            name = (carcom_page[car].find('h2', {'class' : 'title'}).get_text())[5:]
            year = (carcom_page[car].find('h2', {'class' : 'title'}).get_text())[ :4]
            price = carcom_page[car].find('span', {'class': 'primary-price'}).get_text()
            mileage = (carcom_page[car].find('div', {'class': 'mileage'}).get_text()).strip("mi.")

            link = requests.get('https://www.cars.com/' + carcom_page[car].find('a').get('href')).text
            x = BeautifulSoup(link, 'lxml')

            try:
                car_location = x.find('div', {'class' : 'dealer-address'}).get_text()
            except:
                car_location = x.find('div', {'class' : 'dealer-address'}).get_text()
            else:
                car_location = "N/A"

            try:
                number_of_accidents = x.find('dd', {'data-qa' : 'accidents-or-damage-value'})
            except:
                number_of_accidents = "N/A"

            car = {
                "Name": name,
                "Year": year,
                "Mileage": mileage,
                "Location": car_location,
                "Number of Accidents": number_of_accidents,
                "Price": price,
                "Link": link

            }
            cars.append(car)

    return pd.DataFrame(cars)

def main():
   
    get_true_car = scrape_truecar(true_car)
    get_carcom = scrape_carscom(carcom)

    print(get_true_car)
    print(get_carcom)
   
    end = time.time()
    ttime = end - start


    print(ttime)
     
if __name__ == "__main__":
    main()

