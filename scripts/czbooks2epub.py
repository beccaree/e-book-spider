import sys
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from ebooklib import epub
import uuid

# epublib docs: https://docs.sourcefabric.org/projects/ebooklib/en/latest/tutorial.html#introduction

def extract_chapter(chapter_url):
    cPage = requests.get('https:' + chapter_url)
    cPage.raise_for_status()
    cSoup = BeautifulSoup(cPage.content, 'html.parser')
    
    contentDiv = cSoup.find('div', class_='content')
    assert contentDiv, 'could not find content for ' + cTitle

    return str(contentDiv)

if len(sys.argv) != 2:
    print('command format error: python czbooks2epub.py [czBooks url]')
    exit()

targetUrl = sys.argv[1]

page = requests.get(targetUrl)
page.raise_for_status()
soup = BeautifulSoup(page.content, 'html.parser')

# book info
infoSection = soup.find('div', class_='info')
title = infoSection.find('span', class_='title').text.strip()
author = infoSection.find('span', class_='author').find('a').text.strip()
description = soup.find('div', class_='description').text.strip()
print('%sby%s' % (title, author))

# create epub book
book = epub.EpubBook()
book.set_identifier('czbooks_%s' % uuid.uuid4())
book.set_title(title)
book.set_language('zh')
book.add_author(author)
book.add_metadata('DC', 'description', description)

# read all chapters from main page
chapterList = soup.find('ul', id='chapter-list')
assert chapterList, 'chapters not found'

chapters = []

for i, c in enumerate(tqdm(chapterList.find_all('a', href=True))):
    cTitle = c.text.strip()
    cUrl = c['href']

    chapter = epub.EpubHtml(title=cTitle, file_name='chapter_%d.xhtml' % i, lang='zh')
    content = extract_chapter(cUrl)
    chapter.set_content(content)

    book.add_item(chapter)
    chapters.append(chapter)

# Set the TOC
book.toc = (
    epub.Link("chapter_0.xhtml", "Chapter 0", "chapter0"),
    (epub.Section('Chapters'), chapters[1::])
)
# add navigation files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
book.spine = chapters

epub.write_epub('book.epub', book, {})

print('Done!')
