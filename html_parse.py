import os
import requests
from bs4 import BeautifulSoup
from urllib import request


site = 'http://example.com'

response = requests.get(site).text
#response = response.encode('latin-1')

soup = BeautifulSoup(response, 'html.parser')

link_tags = soup.find_all('link')
script_tags = soup.find_all('script')
count = 0


header = soup.find_all('div', class_='header')
footer = soup.find_all('div', class_='footer')
menu = soup.find_all('div', class_='bmMenu')
call_to_action = soup.find_all('div', class_='callToActionAllArea')
[div.extract() for div in menu]
[div.extract() for div in header]
[div.extract() for div in footer]
[div.extract() for div in call_to_action]


links = [link['href'] for link in link_tags]
for link in links:
    if '.css' in link:
        count += 1
        link_url = 'http://example.com'+link
        request.urlretrieve(link_url, filename=f'offer/style{count}.css')


with open(f'offer/{site[34:]}.css', 'w') as style_file:
    for file in os.listdir('offer'):
        if '.css' in file:
            with open(f'offer/{file}', 'r+') as f:
                for line in f:
                    style_file.write(line)


with open('offer/result.html', 'w+', encoding='utf-8') as result_file:
    img_tags = soup.find_all('img')
    pics = [img['src'] for img in img_tags]
    for pic in pics:
        if '//' not in pic:
            count += 1
            pic_url = 'http://example.com' + pic
            request.urlretrieve(pic_url, filename=f"offer/images/{os.path.basename(pic_url)}")
    for link in img_tags:
        new_link = link['src']
        new_link = new_link.split('/')
        new_link = os.path.join('images/', new_link[-1])
        link['src'] = new_link
    result = soup.body
    result_file.write(str(result))





