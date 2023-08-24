import sys
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

if len(sys.argv) != 2:
    print('command format error: python czbooks2txt.py [czBooks url]')
    exit()

targetUrl = sys.argv[1]

page = requests.get(targetUrl)
page.raise_for_status()
soup = BeautifulSoup(page.content, 'html.parser')

# book info
infoSection = soup.find('div', class_='info')
title = infoSection.find('span', class_='title').text.strip()
author = infoSection.find('span', class_='author').find('a').text.strip()
fileName = title + 'by' + author + '.txt'
print(fileName)

chapters = soup.find('ul', id='chapter-list')
assert chapters, 'chapters not found'

with open(fileName, 'w', encoding='utf-8') as f:
    for c in tqdm(chapters.find_all('a', href=True)):
        cTitle = c.text.strip()
        cUrl = c['href']

        cPage = requests.get('https:' + cUrl)
        cPage.raise_for_status()
        cSoup = BeautifulSoup(cPage.content, 'html.parser')
        
        contentDiv = cSoup.find('div', class_='content')
        assert contentDiv, 'could not find content for ' + cTitle
        f.write(contentDiv.text)
        f.write('\n\n')

print('Done!')
