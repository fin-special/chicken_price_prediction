from email.errors import StartBoundaryNotFoundDefect
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


#웹드라이버 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)


def getUrl(startdate,enddate,urlList,filename,query,y,x):
    
    wd = webdriver.Chrome(ChromeDriverManager().install())
    
    for i in range(1,4001,10):
        try: 

            # wd.get(f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%8B%AD%EA%B3%A0%EA%B8%B0%20%EA%B0%80%EA%B2%A9&sort=0&photo=0&field=0&pd=3&ds={startdate}&de={enddate}&cluster_rank=11&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20210101to20211231,a:all&start={i}')
            wd.get(f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={query}&sort=0&photo=0&field=0&pd=3&ds={startdate}&de={enddate}&cluster_rank=11&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from20210101to20211231,a:all&start={i}')
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
    print('---------------')
    print(f'{y}년{x}월뉴스url 저장완료')
    print('---------------')
    # print(f'url 길이 : {len(urlList)}')
    # print('---------------')

def getNavernewsInfo(filename,urlList,dateList,titleList,contentList,i,y,x):

    wd = webdriver.Chrome(ChromeDriverManager().install())
    
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
    df = df.drop_duplicates(subset='기사제목')      #기사제목 중복 제거
    df.to_csv(filename)
    
    print('---------------')
    print(f'{y}년{x}월뉴스기사 저장완료')
    print('---------------')
    # print(f'url 길이 : {len(urlList)}')
    # print(f'뉴스 길이 : {len(titleList)}')
    # print('---------------')



def main():
    i = 1
    query = input(f'검색어를 입력하세요 : ')        # 혹시모를 범용성을 위해 검색어 입력 방식으로 전환
    startyear = int(input(f'검색시작연도 : '))     # 검색시작연도
    endyear = int(input(f'검색종료연도(1년만 검색시 검색시작연도와 동일) : '))       # 검색종료연도(1년만 검색시 검색시작연도와 동일)
    for y in range(startyear,endyear+1):
        for x in range(1,13):
            if x < 10:
                startdate=f'{y}.0{x}.01'
                enddate=f'{y}.0{x}.31'
            else:
                startdate = f'{y}.{x}.01'
                enddate=f'{y}.{x}.31'
            urlList = []
            dateList = []
            titleList = []
            contentList = []
            # query = '닭고기 가격'
            filename1 = f'./네이버뉴스크롤링결과/{query.replace(" ", "_")}_{y}년{x}월url.csv'
            filename2 = f'./네이버뉴스크롤링결과/{query.replace(" ", "_")}_{y}년{x}월뉴스.csv'

            getUrl(startdate,enddate,urlList,filename1,query,y,x)
            getNavernewsInfo(filename2,urlList,dateList,titleList,contentList,i,y,x)

            print(f'{y}년{x}월 완료')

        print(f'{y}년 전체 완료')
    print('---------------')
    print('목표크롤링 최종 완료')
    print('---------------')
if __name__ == '__main__':
    main()
