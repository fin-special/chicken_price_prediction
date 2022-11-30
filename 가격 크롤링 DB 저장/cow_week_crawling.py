from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pymysql


url = 'https://www.ekapepia.com/priceStat/distrPriceBeef.do?menuId=menu100033&boardInfoNo='
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
    cow_price_list = []
    for j in range (1):
        try : 
            cow_price = soup.find('tbody')('th')[i].text
            cow_price_list.append(cow_price)
            cow_price = soup.find('tbody')('tr')[i]('td')[3].text.replace(',','').split('\n')[3]
            cow_price = pd.to_numeric(cow_price)
            cow_price_list.append(cow_price)
        except : 
            cow_price_list.append(cow_price)


    sql = "INSERT INTO cow( date, 도매가격 ) VALUES (%s, %s)"
    val = cow_price_list
    
    try :
        mycursor.execute(sql,val)
        mydb.commit()
    except :
        continue

mydb.close()
