import requests
from bs4 import BeautifulSoup

url = 'https://www.citilink.ru/catalog/computers_and_notebooks/parts/cpu/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

processors = soup.find_all('div', {'class': 'product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing'})
for processor in processors:
    name = processor.find('div', {'class': 'ProductCardHorizontal__title'}).text.strip()
    price = processor.find('div', {'class': 'ProductCardHorizontal__price-current'}).text.strip()
    print(name, price)