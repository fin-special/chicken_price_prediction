import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

keyword = input('뉴스 키워드를 입력하세요 : ')

def news_crawling(query):
    startdate = (datetime.today() + timedelta(days=-7)).strftime("%Y.%m.%d")
    enddate = datetime.today().strftime("%Y.%m.%d")

    url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={query}&sort=0&photo=0&field=0&pd=1&ds={startdate}&de={enddate}&cluster_rank=101&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:1w,a:all&start=1'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    news = soup.find_all('a', class_ = 'news_tit')

    result = []

    try:
        for i in range(11):
            title = news[i].text
            url = news[i]['href']

            data = {'title' : title,
                    'url' : url}

            result.append(data)

    except:
        pass
    return print(result)

news_crawling(keyword)