from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pymysql


url = 'https://www.ekapepia.com/priceStat/distrPricePork.do'
res = requests.get(url)

soup = BeautifulSoup(res.text)


mydb = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '1234',
    db = 'price',
    charset='utf8'
)


mycursor = mydb.cursor()

for i in range(4,-1,-1):
    pork_price_list = []
    for j in range (1):
        try : 
            pork_price = soup.find('tbody')('th')[i].text
            pork_price_list.append(pork_price)
            pork_price = soup.find('tbody')('tr')[i]('td')[1].text.replace(',','').split('\n')[2]
            pork_price = pd.to_numeric(pork_price)
            pork_price_list.append(pork_price)
        except : 
            pork_price_list.append(pork_price)

    sql = "INSERT INTO pork( date, 도매가격 ) VALUES (%s, %s)"
    val = pork_price_list
    
    try :
        mycursor.execute(sql,val)
        mydb.commit()
    except :
        continue

mydb.close()
