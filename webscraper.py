from bs4 import BeautifulSoup
import requests
import pandas as pd

cars = []

true_car = requests.get("https://www.truecar.com/used-cars-for-sale/listings/?page=1").text

soup = BeautifulSoup(true_car, 'lxml')

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

total_page_numbers = range(int(get_total_pages(soup) / 33))

for page_number in total_page_numbers:

    true_car = requests.get(f"https://www.truecar.com/used-cars-for-sale/listings/?page={page_number}").text

    soup = BeautifulSoup(true_car, 'lxml')

    test = soup.find_all('div', {'data-test' : 'cardContent'})

    links = soup.find_all('a', {'data-test' : 'cardContent'})
    #print(links)

    #print(test[3].find('div', {}).get_text())
    for car in range(len(test)):
        name = test[car].find('span', {'class':'truncate'}).get_text()
        year = test[car].find('span', {'class' : 'vehicle-card-year text-xs'}).get_text()
        price = test[car].find('div', {'data-test' : 'vehicleCardPricingBlockPrice'}).get_text()
        if price.count('$') > 1:
            
            price = price[price.index('$',1):]

        link = test[car].find('a').get('href')
        car = {
            "Name": name,
            "Year": year,
            "Price": price,
            "Link": link
        }
        cars.append(car)
        
df = pd.DataFrame(cars)

print(df)
        #print(year, name, price, link)
    #print(len(test))
df.to_excel('test.xlsx', index=False)
