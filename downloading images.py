import sqlite3
import time
from pathlib import Path
import requests

def selectExecute(req):
    conn = sqlite3.connect('configurator_v1.db')
    cur = conn.cursor()
    cur.execute(req)
    entries = cur.fetchall()
    conn.close()
    return entries

table_name = 'power_supply_units'

data = selectExecute(f'SELECT image FROM {table_name};')
urls = []
for record in data:
    if 'http' in record[0]:
        urls.append(record[0])
    else:
        urls.append('https://n-katalog.ru' + record[0])
urls = set(urls)
for url in urls:
    symbol_index = None
    for symbol_index in range(len(url)-1, 0, -1):
        if url[symbol_index-1] == '/':
            break
    file_name = url[symbol_index:]

    time.sleep(0.5)
    resp = requests.get(url)
    print(resp.status_code)

    path = Path('images', table_name, file_name)
    with open(path, 'wb') as file:
        file.write(resp.content)
