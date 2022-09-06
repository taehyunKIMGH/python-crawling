from unittest import skip
import requests
import pandas
from bs4 import BeautifulSoup
from urllib.request import urlopen

chart = pandas.DataFrame()

url = "https://movie.naver.com/movie/running/premovie.naver?order=reserve#"
html = urlopen(url).read()
soup = BeautifulSoup(html,'html.parser')

found = soup.find('ul',{'class':'lst_detail_t1'}).find_all('li')

title = []
dirt = []
type = []
chrt = []
date = []

for a in found:
  title.append((a.dl.dt.a).text.replace('',''))

cnt=0

for dir in found:
  direct = dir.find('dl',{'class':'lst_dsc'}).find('dl',{'class':'info_txt1'}).find_all('span',{'class':'link_txt'})
  count = 0
  cnt+=1
  for directer in direct:
    if directer.text.strip() !='':
      count +=1
      if count==1:
          type.append(directer.text.strip().replace('\r','').replace('\n','').replace('\t',''))
      if count==2:
          dirt.append(directer.text.strip().replace('\r','').replace('\n','').replace('\t',''))
      if count==3:
          chrt.append(directer.text.strip().replace('\r','').replace('\n','').replace('\t',''))


for  d in found:
    day = d.find('dl',{'class':'lst_dsc'}).find('dl',{'class':'info_txt1'}).find_all('dd')
    count=0
    for D in day:
        count+=1
        if count == 1:
            date.append((D.text.replace('\r','').replace('\n','').replace('\t','').replace('|',' ')
                        .replace('액션','').replace('코미디','').replace('애니메이션','').replace('범죄','').replace('드라마','').replace('판타지','').replace('다큐멘터리','').replace('뮤지컬','').replace('공연실황','')
                        .replace('전쟁','').replace('스릴러','').replace('공포','').replace('멜로/로맨스','').replace('미스터리','').replace('SF','').replace(',','').replace('가족','').replace('모험','').replace('개봉','').strip()).split(' '))

print(len(title),len(dirt),len(type),len(date))

for n in range(len(title)):
  data = {
      '영화 제목' : title[n],
      '장르' : type[n],
      '상영시간, 개봉일' : date[n]
    }
  chart = chart.append(data, ignore_index = True)
chart.to_excel('영화 개봉작.xlsx')