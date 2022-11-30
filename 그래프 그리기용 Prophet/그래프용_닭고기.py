import pandas as pd
from matplotlib import font_manager, rc
import pymysql
import datetime
from prophet import Prophet
import functools as ft

data = pd.read_csv('./닭고기가격.csv',index_col=0)
data['date'] = pd.to_datetime(data['date'])

mydb = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '1234',
    db = 'price',
    charset='utf8'
)

cursor = mydb.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * FROM price.chicken ORDER BY 1 DESC LIMIT 6")
result = cursor.fetchall()


df = pd.DataFrame(result)
df.drop(columns='요일',inplace=True)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date',ascending=True)

tomorrow = df['date'][-1:]  + datetime.timedelta(days=1)
tomorrow = pd.DataFrame(tomorrow)

df = pd.merge(df,tomorrow,on='date',how='outer')
df = df.fillna(method='ffill')

data = pd.concat((data,df),axis=0)
data['date'] = pd.to_datetime(data['date'])
data = data.sort_values(by='date', ascending=True)
data = data.drop_duplicates(subset=['date'],keep='first')
data = data[-2220:]
data.to_csv('./닭고기가격.csv')

data_5_6 = data[['date', '5_6호']]
data_5_6 = data_5_6.rename(columns=({'date':'ds','5_6호':'y'}))

data_7_8 = data[['date', '7_8호']]
data_7_8 = data_7_8.rename(columns=({'date':'ds','7_8호':'y'}))

data_9_10 = data[['date', '9_10호']]
data_9_10 = data_9_10.rename(columns=({'date':'ds','9_10호':'y'}))

data_11 = data[['date', '11호']]
data_11 = data_11.rename(columns=({'date':'ds','11호':'y'}))

data_12 = data[['date', '12호']]
data_12 = data_12.rename(columns=({'date':'ds','12호':'y'}))

data_13_16 = data[['date', '13_16호']]
data_13_16 = data_13_16.rename(columns=({'date':'ds','13_16호':'y'}))

Bok_nal = pd.DataFrame({
'holiday': 'Bok_nal',
'ds': pd.to_datetime(['2016-07-17', '2016-07-27', '2016-08-16',
                      '2017-07-12', '2017-07-22', '2017-08-11',
                      '2018-07-17', '2018-07-27', '2018-08-16',
                      '2019-07-12', '2019-07-22', '2019-08-11',
                      '2020-07-16', '2020-07-26', '2020-08-15',
                      '2021-07-11', '2021-07-21', '2021-08-10',
                      '2022-07-16', '2022-07-26', '2022-08-15'
                      ]),
'lower_window': 0,
'upper_window': 1,
})

AI = pd.DataFrame({
'holiday': 'AI',
'ds': pd.to_datetime([
    '2016-11-16', '2016-11-22', '2016-11-23', '2016-11-26', 
    '2016-11-27', '2016-11-28', '2016-11-29', '2016-11-30', '2016-12-01',
    '2016-12-02', '2016-12-03', '2016-12-04', '2016-12-05', '2016-12-06', 
    '2016-12-07', '2016-12-08', '2016-12-09', '2016-12-10', '2016-12-11', 
    '2016-12-12', '2016-12-13', '2016-12-14', '2016-12-15', '2016-12-16',
    '2016-12-17', '2016-12-18', '2016-12-19', '2016-12-20', '2016-12-21', 
    '2016-12-22', '2016-12-23', '2016-12-24', '2016-12-25', '2016-12-26', 
    '2016-12-27', '2016-12-28', '2016-12-29', '2016-12-30',
    '2017-01-01', '2017-01-03', '2017-01-05', '2017-01-07', '2017-01-08', 
    '2017-01-09', '2017-01-10', '2017-01-12', '2017-01-14', '2017-01-20', 
    '2017-01-21', '2017-01-24', '2017-02-06', '2017-02-09', '2017-02-22', 
    '2017-02-27', '2017-03-01', '2017-03-02', '2017-03-03', '2017-03-06', 
    '2017-03-17', '2017-03-19', '2017-03-22', '2017-03-23', '2017-03-26', 
    '2017-03-27', '2017-03-29', '2017-04-02', '2017-06-03', '2018-01-03', 
    '2018-01-26', '2018-01-27', '2018-02-04', '2018-02-08', '2018-03-16', 
    '2018-03-17',
    '2020-12-06', '2020-12-12', '2020-12-14', '2020-12-16', '2020-12-21', 
    '2020-12-22', '2020-12-25', '2020-12-28', '2020-12-28', '2020-12-29',
    '2020-12-29', '2020-12-31', '2021-01-01', '2021-01-03', '2021-01-04',
    '2021-01-08', '2021-01-11', '2021-01-12', '2021-01-11', '2021-01-12',
    '2021-01-13', '2021-01-18', '2021-01-21', '2021-01-22', '2021-01-23',
    '2021-01-26', '2021-01-26', '2021-01-27', '2021-01-29', '2021-01-30',
    '2021-01-31', '2021-02-01', '2021-02-07', '2021-02-09', '2021-02-12', 
    '2021-02-13', '2021-02-15', '2021-02-17', '2021-02-22', '2021-02-23',
    '2021-02-26', '2021-03-10', '2021-03-10', '2021-03-11', '2021-11-19',
    '2021-12-03', '2021-12-05', '2021-12-11', '2021-12-14', '2021-12-16',
    '2021-12-20', '2021-12-23',
    '2022-01-21', '2022-01-23', '2022-10-21', '2022-11-14', '2022-11-15',
    '2022-11-17']),
'lower_window': 0,
'upper_window': 1,
})

holidays = pd.concat((Bok_nal, AI))

# 5,6호 닭 예측
m = Prophet(holidays=holidays)
m.add_country_holidays(country_name='KR').fit(data_5_6)
future = m.make_future_dataframe(periods=30,freq='D') # 주 단위로, 4주 가격 예측 실시
forecast = m.predict(future)
predict_size_5_6 = forecast[['ds','yhat']]

# 7,8호 닭 예측
m = Prophet(holidays=holidays)
m.add_country_holidays(country_name='KR').fit(data_7_8)
future = m.make_future_dataframe(periods=30,freq='D') # 주 단위로, 4주 가격 예측 실시
forecast = m.predict(future)
predict_size_7_8 = forecast[['ds','yhat']]

# 9,10호 닭 예측
m = Prophet(holidays=holidays)
m.add_country_holidays(country_name='KR').fit(data_9_10)
future = m.make_future_dataframe(periods=30,freq='D') # 주 단위로, 4주 가격 예측 실시
forecast = m.predict(future)
predict_size_9_10 = forecast[['ds','yhat']]

# 11호 닭 예측
m = Prophet(holidays=holidays)
m.add_country_holidays(country_name='KR').fit(data_11)
future = m.make_future_dataframe(periods=30,freq='D') # 주 단위로, 4주 가격 예측 실시
forecast = m.predict(future)
predict_size_11 = forecast[['ds','yhat']]

# 12호 닭 예측
m = Prophet(holidays=holidays)
m.add_country_holidays(country_name='KR').fit(data_12)
future = m.make_future_dataframe(periods=30,freq='D') # 주 단위로, 4주 가격 예측 실시
forecast = m.predict(future)
predict_size_12 = forecast[['ds','yhat']]

# 13,16호 닭 예측
m = Prophet(holidays=holidays)
m.add_country_holidays(country_name='KR').fit(data_13_16)
future = m.make_future_dataframe(periods=30,freq='D') # 주 단위로, 4주 가격 예측 실시
forecast = m.predict(future)
predict_size_13_16 = forecast[['ds','yhat']]

dfs = [predict_size_5_6,predict_size_7_8,predict_size_9_10,predict_size_11,predict_size_12,predict_size_13_16]
df_final = ft.reduce(lambda left,right : pd.merge(left,right, on='ds',how='left'), dfs)

col = ['date','5_6호', '7_8호', '9_10호', '11호', '12호', '13_16호']
df_final.columns = col

df_final['평균가격'] = df_final.mean(axis=1)

df_final = df_final[-30:]
forecast.to_csv('./그래프용_닭고기가격예측.csv')
print(df_final)