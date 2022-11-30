import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import pymysql

query = "돼지고기 가격"
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

mydb = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '1234',
    db = 'price',
    charset='utf8'
)

mycursor = mydb.cursor()

for i in range(10):

    title = result[i]['title']
    url = result[i]['url']

    sql = "INSERT INTO news_pork( title,url ) VALUES (%s, %s)"
    val = (title,url)


    mycursor.execute(sql,val)
    mydb.commit()

mydb.close()