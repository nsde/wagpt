"""Module for searching the web to answer questions."""

import random
import bs4
import requests
import html2text

import config

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 
    'Accept-Encoding': 'gzip, deflate', 
    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7', 
    'Upgrade-Insecure-Requests': '1', 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 
}

def search_whoogle(instance: str, query: str) -> str:
    """Performs a Google search with the given Whoogle instance and returns the result in plain text."""

    url = f'{instance}/search?q={query}'
    html = requests.get(url, timeout=3, headers=HEADERS).text

    soup = bs4.BeautifulSoup(html, 'html.parser')
    soup = soup.find('div', {'id': 'main'})

    tags = ['img', 'video', 'svg', 'script', 'style', 'iframe', 'audio', 'canvas', 'map', 'noscript', 'a']
    for tag in tags:
        for match in soup.findAll(tag):
            match.decompose()

    for match in soup.findAll(True, {'class': 'r0bn4c'}):
        match.decompose()

    # remove all src and href attributes
    for tag in soup.findAll(True):
        tag.attrs = {}

    html = str(soup)
    html = html.split('Related searches', maxsplit=1)[0]

    h2t = html2text.HTML2Text()
    h2t.ignore_links = True
    plain_text = h2t.handle(html)
    
    for char in ['*', '_', '~', '`']:
        plain_text = plain_text.replace(char, '')

    plain_text = plain_text.replace('\n\n', '\n')
    lines = plain_text.split('\n')

    # remove lines without alnum characters
    plain_text = '\n'.join([line for line in lines if any(char.isalnum() for char in line)])

    return plain_text.replace('See results about\n', '').replace(' ...', '')

def results_for_ai(query: str) -> str:
    """Performs a Google search and returns the result in a format that AI can understand (plain text."""

    while True:
        instance = random.choice(config.read('search')['instances'])
        try:
            result = search_whoogle(instance, query)
            return result
        except requests.exceptions.Timeout:
            continue

if __name__ == '__main__':
    res = results_for_ai('tallest mountain in europe')
    print(res)
