import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import pymysql
import datetime
from prophet import Prophet

data = pd.read_csv('./돼지고기가격.csv',index_col=0)
data['date'] = pd.to_datetime(data['date'])

mydb = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '1234',
    db = 'price',
    charset='utf8'
)

cursor = mydb.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * FROM price.pork ORDER BY 1 DESC LIMIT 5")
result = cursor.fetchall()

df = pd.DataFrame(result)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date',ascending=True)

days_1 = pd.DataFrame(df['date'][-1:]  + datetime.timedelta(days=1))
days_2 = pd.DataFrame(df['date'][-1:]  + datetime.timedelta(days=2))
days = pd.concat((days_1,days_2))

df = pd.merge(df,days,on='date',how='outer')
df = df.fillna(method='ffill')

data = pd.concat((data,df),axis=0)
data['date'] = pd.to_datetime(data['date'])
data = data.sort_values(by='date', ascending=True)
data = data.drop_duplicates(subset=['date'], keep='first')
data = data[-2220:]

data = data[['date', '도매가격']]
data = data.rename(columns=({'date':'ds','도매가격':'y'}))

m = Prophet(changepoint_range=0.9,changepoint_prior_scale=0.25)
# m.add_seasonality(name='monthly', period=30.5, fourier_order=5)
m.add_country_holidays(country_name='KR').fit(data)
future = m.make_future_dataframe(periods=30,freq='D') # 주 단위로, 4주 가격 예측 실시
forecast = m.predict(future)

forecast =  forecast[['ds','yhat']][-30:]
forecast.to_csv('./그래프용_돼지고기가격예측.csv')
print(forecast)