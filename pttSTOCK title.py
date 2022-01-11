import requests
from bs4 import BeautifulSoup
import time

today = time.strftime('%m/%d').lstrip('0')

def pttSTOCK(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print('URL ERROR：' + url)
        return
    soup = BeautifulSoup(resp.text, 'html5lib')
    paging = soup.find('div', 'btn-group btn-group-paging').find_all('a')[1]['href']
    articles = []
    rents = soup.find_all('div', 'r-ent')
    for rent in rents:
        title = rent.find('div', 'title').text.strip()
        count = rent.find('div', 'nrec').text.strip()
        date = rent.find('div', 'meta').find('div', 'date').text.strip()
        article = '%s %s:%s' % (date, count, title)
        try:
            if today == date and int(count) >= 0:
                articles.append(article)
        except:
            if today == date and count == '爆':
                articles.append(article)
    if len(articles) != 0:
        for article in articles:
            print(article)
        pttSTOCK('https://www.ptt.cc' + paging)
    else:
        return
        
pttSTOCK('https://www.ptt.cc/bbs/Stock/index.html')
