from konlpy.tag import Okt, Kkma, Komoran
from collections import Counter

import pandas as pd

# 불용어 사전 설정
korean_stopwords_path = './데이터전처리/data/korean_stopwords.txt'
news_stopwords_path = './데이터전처리/data/news_stopwords.txt'


with open(korean_stopwords_path, encoding='utf-8') as f:
    stopwords = f.readlines()
stopwords = [x.strip() for x in stopwords]

with open(news_stopwords_path, encoding='utf8') as s:
    newsstopwords = s.readlines()
news_stopwords = [x.strip() for x in newsstopwords]

for stopword in news_stopwords:
    stopwords.append(stopword)

# 형태소 분리 및 불용어 제거
for i in range(2012, 2022):
    for j in range(1, 13):
        filename = f'./데이터전처리/data/닭고기가격_2012_2021/닭고기_가격_{i}년{j}월뉴스.csv'
        f = open(filename, 'r', encoding='utf-8')
        news = f.read()

        okt = Okt()
        morphs = okt.morphs(news)
        count = Counter(morphs)

        # 1글자 제거
        remove_char_counter = Counter({x : count[x] for x in count if len(x) > 1})
        # print(remove_char_counter)

        remove_char_counter = Counter({x : remove_char_counter[x] for x in count if x not in stopwords})
        # print(remove_char_counter)

        ranked_tags = remove_char_counter.most_common(100)
        # print(ranked_tags)

        # 데이터프레임으로 변환
        ranked_tags_df = pd.DataFrame(ranked_tags, columns=['tags', 'count'])

        # csv로 저장
        ranked_tags_df.to_csv(f'./데이터전처리/pre_data/닭/닭빈도{i}-{j}.csv', index=False)
        print(f'{i}년{j}월 저장완료')
        
    