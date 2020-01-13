import requests
import re
import csv
from bs4 import BeautifulSoup as bs
​
headers = {
    'accept': "*/*",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}
​
base_url = ''
​
​
def hh_parse(base_url: object, headers: object):
    products = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html5lib')
​
        try:
            pagination = soup.find('ul', class_='pagination').find_all('a')['href']
            print(pagination)
            count = int(pagination[-1].text)
            print(count)
            for i in range(count):
                url = f'{base_url}{i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
​
        for url in urls:
            request = session.get(base_url, headers=headers)
            soup = bs(request.content, 'html5lib')
            divs = soup.find_all('div', {'class': 'product-thumb'})
            for div in divs:
                title = div.find('h4').text
                href = div.find('a')['href']
                cod_product = div.find('span').text
                price = div.find('p', {'class': 'price'}).text.replace(' ', '')
                price = re.sub("^\s+|\n|\r|\s+$", '', price)  # Удаляем лишние пробелы и переносы строк
                stock = div.find('p', {'oct-product-stock'}).text
                products.append({
                    'title': title,
                    'href': href,
                    'cod_product': cod_product,
                    'price': price,
                    'stock': stock,
                    'notes': ''
                })
                print('Cпарсено: ' + ' ' + str(len(products)))
    else:
        print('Error!!!')
    return products
​
​
def file_writer(products):
    with open('product_verter.csv', 'w', newline='', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название товара', 'Ссылка на товар', 'Код товара', 'Цена', 'Наличие товара', 'Примечание'))
        for product in products:
            a_pen.writerow((product['title'], product['href'], product['cod_product'], product['price'], product['stock'], product['notes']))
​
​
products = hh_parse(base_url, headers)
file_writer(products)