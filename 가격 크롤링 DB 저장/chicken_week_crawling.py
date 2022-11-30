from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pymysql


url = 'http://www.chicken.or.kr/ch_price/price01.php'
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

for i in range(5,-1,-1):
    chick_price_list = []
    for j in range (8):
        try : 
            chick_price = soup.find('tbody')('tr')[i]('td')[j].text.replace(',','')
            chick_price = pd.to_numeric(chick_price)
            chick_price_list.append(chick_price)
        except : 
            chick_price_list.append(chick_price)

    sql = "INSERT INTO chicken( date, 요일, 5_6호, 7_8호, 9_10호, 11호, 12호, 13_16호 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = chick_price_list
    
    try :
        mycursor.execute(sql,val)
        mydb.commit()
    except :
        continue


mydb.close()
