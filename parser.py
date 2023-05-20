import requests
from bs4 import BeautifulSoup

# URL страницы DNS раздела процессоров
url = 'https://www.dns-shop.ru/catalog/17a8a01d16404e77/processory/'

# Получаем HTML содержимое страницы
response = requests.get(url)
html_content = response.content

# Создаем объект BeautifulSoup для парсинга HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Извлекаем информацию о продуктах
products = []
for product in soup.find_all('div', {'class': 'catalog-item__main-wrapper'}):
    name = product.find('a', {'class': 'catalog-item__name'}).text.strip()
    price_container = product.find('div', {'class': 'product-buy__price'})
    if price_container is None:
        # Если цена не указана, пропускаем продукт
        continue
    price = price_container.find('span', {'class': 'price__current'}).text.strip()
    products.append({'name': name, 'price': price})

# Печатаем результаты парсинга
for product in products:
    print(product['name'], product['price'])
