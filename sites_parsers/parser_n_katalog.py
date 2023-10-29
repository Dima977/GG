import time
import traceback
import requests
from bs4 import BeautifulSoup


def parse(n_katalog_str):
    time.sleep(0.2)  # delay
    url = n_katalog_str.split(',')[1]
    headers = {
        "Accept": "text/html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    }
    shops = []
    try:
        resp = requests.get(url, headers)
        print('code:', resp.status_code)  # log
        soup = BeautifulSoup(resp.text, "html.parser")
        tds = soup.find_all('td', class_='where-buy-price')
        for td in tds:
            if 'dns-shop' in str(td):
                shops.append(['dns', url + '/offer/dns-shop.ru', td.find('a', class_='where-buy-price__link').text.replace('\xa0руб.', '')])
            elif 'citilink' in str(td):
                shops.append(['citilink', url + '/offer/citilink.ru', td.find('a', class_='where-buy-price__link').text.replace('\xa0руб.', '')])
            elif 'kotofoto.ru' in str(td):
                shops.append(['kotofoto.ru', url + '/offer/kotofoto.ru', td.find('a', class_='where-buy-price__link').text.replace('\xa0руб.', '')])
            elif 'xcom-shop.ru' in str(td):
                shops.append(['xcom-shop.ru', url + '/offer/xcom-shop.ru', td.find('a', class_='where-buy-price__link').text.replace('\xa0руб.', '')])
            elif 'xpert.ru' in str(td):
                shops.append(['xpert.ru', url + '/offer/xpert.ru', td.find('a', class_='where-buy-price__link').text.replace('\xa0руб.', '')])
            elif 'oldi.ru' in str(td):
                shops.append(['oldi.ru', url + '/offer/oldi.ru', td.find('a', class_='where-buy-price__link').text.replace('\xa0руб.', '')])
            elif 'kcentr' in str(td):
                shops.append(['kcentr', url + '/offer/kcentr.ru', td.find('a', class_='where-buy-price__link').text.replace('\xa0руб.', '')])
    except Exception:
        print(traceback.format_exc())
    return shops