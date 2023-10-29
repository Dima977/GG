import time
import traceback
import requests
from bs4 import BeautifulSoup

def parse(name):
    time.sleep(0.3)  # delay
    headers = {
        "Accept": "text/html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    shops = []
    try:
        # search
        resp = requests.get(f'https://hardprice.ru/?search={name}&mode=like', headers)
        print('code:', resp.status_code)  # log
        soup = BeautifulSoup(resp.text, "html.parser")
        divs = soup.find_all('div', class_='products-list-v2__item')
        for div in divs:
            div_title = div.find('a', class_='title')
            # todo поиск: name in div_title.text
            # переход на страницу товара, берётся первый товар из результата поиска
            resp_page = requests.get(div_title['href'], headers)
            trs = BeautifulSoup(resp_page.text, "html.parser").find_all('tr')
            for tr in trs:
                try:
                    if tr['data-store'] == "citilink":
                        href = tr.find('a', class_='buy-action text-muted')['href']
                        href = 'www' + href.split('www')[1]
                        shops.append(['citilink', href, tr['data-price']])
                    elif tr['data-store'] == "dns":
                        href = tr.find('a', class_='buy-action text-muted')['href']
                        href = 'www' + href.split('www')[1]
                        shops.append(['dns', href, tr['data-price']])
                    elif tr['data-store'] == "regard":
                        href = tr.find('a', class_='buy-action text-muted')['href']
                        href = 'www' + href.split('www')[1]
                        shops.append(['regard', href, tr['data-price']])
                except KeyError:
                    continue
            break
    except Exception:
        print(traceback.format_exc())
    return shops
