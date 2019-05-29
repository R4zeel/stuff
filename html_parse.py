import os
import requests
from bs4 import BeautifulSoup
from urllib import request

site = 'http://example.com'
response = requests.get(site).text
response = response.encode('utf-8')
soup = BeautifulSoup(response, 'html.parser')
offer_url = site["needed index"] #allows to get specific part of URL to name directory

def links_replacement(tag, path):         #replaces path to js/imgs/css in html body
    tag_list = soup.find_all(tag)
    for link in tag_list:
        if 'src' in link.attrs:
            new_link = link['src'].split('/')
            link['src'] = os.path.join(path, new_link[-1])

def div_extract(class_name):                #removes unnecessary blocks  
    class_name = soup.find_all('div', class_=class_name)
    [div.extract() for div in class_name]

def files_download(tag, attr, path):
    tag_list = soup.find_all(tag)
    items = [link[attr] for link in tag_list if attr in link.attrs]
    for item in items:
        if len(item) > 0:
            if '.' in item[-3] or '.' in item[-4]:         #this line checks for extension in link
                if '//' not in item:
                    item_url = site[:24] + item
                    print(item_url)
                    request.urlretrieve(item_url, filename=f"{path}/{os.path.basename(item_url)}")

div_extract('example_block')


files_download('script', 'src', f'path/to/{offer_url}')
files_download('link', 'href', f'path/to{offer_url}')
files_download('img', 'src', f'path/to{offer_url}/images')

#containing all styles from all css files to one
with open(f'path/to/styles/{offer_url}.css', 'w') as style_file: #added additional 'styles' dir to path to prevent style_file from looping
    for file in os.listdir(f'path/to{offer_url}'):
        if '.css' in file:
            with open(f'path/to/{offer_url}/{file}', 'r+') as f:
                for line in f:
                    style_file.write(line)
for css in os.listdir(f'path/to/{offer_url}/'):  #removes unnecessary css
    if '.css' in css:
        os.remove(f"path/to/{offer_url}/{css}")

with open(f'path/to/{offer_url}/result.html', 'w+', encoding='utf-8') as result_file:
    links_replacement('img', f'/path/to/{offer_url}/images/')
    links_replacement('script', '/path/to/')
    result = soup.body
    result_file.write(str(result))









