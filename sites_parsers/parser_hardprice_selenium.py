from selenium.webdriver.common.by import By
from selenium import webdriver as wd
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium_stealth import stealth


def parse_page(soup):  # окно товара
    shops = []
    trs = soup.find_all('tr')
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
        except (KeyError, IndexError):
            continue
    return shops


def parse(name):
    # todo stealth
    """options = webdriver.ChromeOptions()
    driver = wd.Chrome(options=options)
    stealth(driver=driver,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/83.0.4103.53 Safari/537.36',
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win64",
            webgl_vendor="Intel Inc.",
            fix_hairline=True,  # ?
            run_on_insecure_origins=True,
            )"""
    options = webdriver.FirefoxOptions()
    driver = wd.Firefox(options=options)
    driver.get('https://hardprice.ru/')

    # search
    search = driver.find_element(By.CLASS_NAME, "form-control")
    search.click()
    search.send_keys(name)
    search.send_keys(Keys.RETURN)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # окно результатов поиска
    if 'search' in driver.current_url:
        divs = soup.find_all('div', class_='products-list-v2__item')
        for div in divs:
            div_title = div.find('a', class_='title')
            # todo поиск: name in div_title.text
            driver.get('https://hardprice.ru' + div_title['href'])
            shops = parse_page(BeautifulSoup(driver.page_source, "html.parser"))
            driver.close()
            return shops
    else:  # поиск сразу выдал один товар
        shops = parse_page(BeautifulSoup(driver.page_source, "html.parser"))
        driver.close()
        return shops
