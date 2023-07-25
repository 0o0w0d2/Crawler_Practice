import requests
from bs4 import BeautifulSoup

# 특정 단어에 대해서 블로그 상위 3개 글 제목 크롤링하는 함수 만들기
def wordCrawler(word) :
    data = requests.get(f'https://search.naver.com/search.naver?query={word}&nso=&where=blog&sm=tab_opt')
    soup = BeautifulSoup(data.text.replace('\\', ''), 'html.parser')
    return soup.select('a.api_txt_lines')[0].text, soup.select('a.api_txt_lines')[1].text, soup.select('a.api_txt_lines')[2].text

print(wordCrawler('고양이'))

# infinite scroll이 적용된 경우 글 제목 30개를 연달아서 크롤링하는 함수
# 네이버의 경우 start에서 30개만큼의 글을 가져옴
def infiCrawler(word, start) :
    data = requests.get(f'https://s.search.naver.com/p/blog/search.naver?where=blog&sm=tab_pge&api_type=1&query={word}&rev=44&start={start}&dup_remove=1&post_blogurl=&post_blogurl_without=&nso=&nlu_query=%7B%22r_category%22%3A%2216%22%7D&dkey=0&source_query=&nx_search_query={word}&_callback=viewMoreContents')
    soup = BeautifulSoup(data.text.replace('\\', ''), 'html.parser')
    list = []
    for i in range(0, len(soup.select('a.api_txt_lines'))) :
        list.append(soup.select('a.api_txt_lines')[i].text)
    return list

print(infiCrawler('고양이', 32))


# 특정 단어를 검색했을 때 상위 5개 블로그 이름
def best5BlogNameCrawler(word):
    data = requests.get(f'https://search.naver.com/search.naver?query={word}&nso=&where=blog&sm=tab_opt')
    soup = BeautifulSoup(data.text.replace('\\', ''), 'html.parser')
    list = []
    for i in range(0, 5) :
        list.append(soup.select('a.sub_txt.sub_name')[i].text)
    return list

print(best5BlogNameCrawler('고양이'))

# 특정 단어를 검색했을 때 상위 5개 블로그 주소
def best5BlogUrlCrawler(word):
    data = requests.get(f'https://search.naver.com/search.naver?query={word}&nso=&where=blog&sm=tab_opt')
    soup = BeautifulSoup(data.text.replace('\\', ''), 'html.parser')
    list = []
    for i in range(0, 5) :
        list.append(soup.select('a.sub_txt.sub_name')[i]['href'])
    return list

print(best5BlogUrlCrawler('고양이'))

# 블로그 상위 5개 이미지 수집
def best5BlogPicCrawler(word):
    data = requests.get(f'https://search.naver.com/search.naver?query={word}&nso=&where=blog&sm=tab_opt')
    soup = BeautifulSoup(data.text.replace('\\', ''), 'html.parser')
    list = []
    for i in range(0, 5) :
        list.append(soup.select('img.thumb.api_get')[i]['src'])
    return list

print(best5BlogPicCrawler('고양이'))

# 상위 ~~개 일반화하기 => 함수의 매개변수로 ~~개도 추가하기
