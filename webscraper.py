from bs4 import BeautifulSoup
import requests

cars = []
page = 1

while(page > )
true_car = requests.get(f"https://www.truecar.com/used-cars-for-sale/listings/?page=1").text

soup = BeautifulSoup(true_car, 'lxml')

#print(soup.find_all(''))
#print(soup.contents)

test = soup.find_all('div', {'data-test' : 'cardContent'})

links = soup.find_all('a', {'data-test' : 'cardContent'})
print(links)


#print(test[3].find('div', {}).get_text())
for car in range(len(test)):
    name = test[car].find('span', {'class':'truncate'}).get_text()
    year = test[car].find('span', {'class' : 'vehicle-card-year text-xs'}).get_text()
    price = test[car].find('div', {'data-test' : 'vehicleCardPricingBlockPrice'}).get_text()
    link = test[car].find('a').get('href')
    cars.append(name)

    #print(year, name, price, link)
#print(len(test))

new_page = soup.find_all('li', {'data-test' : 'paginationDirectionalItem'})
print(len(new_page))
next_page = new_page[1].find('a').get('href')

total_page_numbers = ""

for char in next_page:
    if char.isdigit():
        total_page_numbers = total_page_numbers + char
print(total_page_numbers)

total_page_numbers = int(total_page_numbers) 

print(total_page_numbers)

for x in range(int(total_page_numbers / 3)):
    true_car = requests.get(f"https://www.truecar.com/used-cars-for-sale/listings/?page={x}")

print(len(cars))
