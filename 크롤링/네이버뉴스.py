from email.errors import StartBoundaryNotFoundDefect
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

#branch test 

# 유빈테스트

def getUrl(startdate,enddate,urlList,filename):
    
    wd = webdriver.Chrome('./chromedriver.exe')
    
    for i in range(1,4001,10):
        try: 

            wd.get(f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%8B%AD%EA%B3%A0%EA%B8%B0%20%EA%B0%80%EA%B2%A9&sort=0&photo=0&field=0&pd=3&ds={startdate}&de={enddate}&cluster_rank=11&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20210101to20211231,a:all&start={i}')
            # 마지막페이지 판단하기
            final = wd.find_elements(By.CSS_SELECTOR, 'a.btn_next')
            checkFinal = final[0].get_attribute('href')
            if type(checkFinal) != str:
                break

            src1 = wd.find_elements(By.CSS_SELECTOR,'div.info_group > a.info')
            src2 = wd.find_elements(By.CSS_SELECTOR,'div.info_group > a.info.press')
            total = list(set(src1)- set(src2))
            for url in total:
                urlList.append(url.get_attribute('href'))
                # print('urlList길이',len(urlList))
        except Exception as e:
            print(e)

    wd.quit()
    # 중복 url 제거
    urlList = list(set(urlList))
    df = pd.DataFrame({'url':urlList})
    df.to_csv(filename)

def getNavernewsInfo(filename,urlList,dateList,titleList,contentList,i):

    wd = webdriver.Chrome('./chromedriver.exe')
    
    for url in urlList:
        try:
            wd.get(url)
            time.sleep(0.1)
            req = wd.page_source
            soup = BeautifulSoup(req,'html.parser')

            # 날짜
            date = soup.select('span.media_end_head_info_datestamp_time')
            dateList.append(date[0].text)
            # 기사제목
            title = soup.select('h2.media_end_head_headline')
            title =  title[0].text
            titleList.append(title)
            # 기사내용
            text = soup.select('#dic_area ')
            text = text[0].text
            contentList.append(text.replace('\n',''))
        except Exception as e:
            i += 1
            print('다음기사',i)
            continue
    wd.quit()
    df = pd.DataFrame({'날짜':dateList, '기사제목':titleList, '기사내용':contentList})
    df = df.drop_duplicates(subset='기사제목')
    df.to_csv(filename)


def main():
    i = 1
    for x in range(1,10):
        if x < 10:
            startdate=f'2019.0{x}.01'
            enddate=f'2019.0{x}.31'
        else:
            startdate = f'2019.{x}.01'
            enddate=f'2019.{x}.31'
        urlList = []
        dateList = []
        titleList = []
        contentList = []
        filename1 = f'2019년{x}월url.csv'
        filename2 = f'2019년{x}월뉴스.csv'

        getUrl(startdate,enddate,urlList,filename1)
        getNavernewsInfo(filename2,urlList,dateList,titleList,contentList,i)



if __name__ == '__main__':
    main()
