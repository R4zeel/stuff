import os
import requests
from bs4 import BeautifulSoup
from urllib import request

url_input = input('input URL: ')
default = 'http://example.com'
site = default + url_input
response = requests.get(site).text
# response = response.encode('latin-1')
# response = response.encode('utf-8')
soup = BeautifulSoup(response, 'xml')
offer_url = site[# needed index]
offers_path = f'path/to/{offer_url}'
if os.path.exists(offers_path):
    pass
else:
    os.mkdir(offers_path)


def links_replacement(tag):
    tag_list = soup.find_all(tag)
    for link in tag_list:
        if 'src' in link.attrs:
            new_link = link['src'].split('/')
            link['src'] = os.path.join(f'/{offers_path}/', new_link[-1])


def div_extract(class_name):
    class_name = soup.find_all('div', class_=class_name)
    [div.extract() for div in class_name]


def files_download(tag, attr):
    tag_list = soup.find_all(tag)
    items = [link[attr] for link in tag_list if attr in link.attrs]
    for item in items:
        if len(item) > 0:
            if '.' in item[-3] or '.' in item[-4]:
                if 'http' in item:
                    if 'google' not in item:  # avoiding google scripts
                        request.urlretrieve(item, filename=f"{offers_path}/{os.path.basename(item)}")
                elif '//' in item:
                    if 'google' not in item:
                        request.urlretrieve('https:'+item, filename=f"{offers_path}/{os.path.basename(item)}")
                elif '//' not in item:
                    item_url = site[# needed index] + item
                    request.urlretrieve(item_url, filename=f"{offers_path}/{os.path.basename(item_url)}")


files_download('script', 'src')
files_download('link', 'href')
files_download('img', 'src')

div_extract('header')
div_extract('footer')

with open(f'path/to/{offer_url}.css', 'w') as style_file:
    for file in os.listdir(f'{offers_path}'):
        if '.css' in file:
            with open(f'{offers_path}/{file}', 'r+') as f:
                for line in f:
                    style_file.write(line)
for css in os.listdir(f'{offers_path}/'):
    if '.css' in css:
        os.remove(f"{offers_path}/{css}")

with open(f'{offers_path}/result_{offer_url}.html', 'w+', encoding='utf-8') as result_file:
    links_replacement('img')
    links_replacement('script')
    result = soup.body
    result_file.write(str(result))




