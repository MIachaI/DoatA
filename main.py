from bs4 import BeautifulSoup
import requests
import re

url = 'https://pl.dotabuff.com/players/41771279/matches'
matchesList = []
r = requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"})

soup = BeautifulSoup(r.text, 'html.parser')

for a in soup.find_all(href=re.compile('.matches\/\d*')):
    matchesList.append(a['href'])

#print(matchesList)
nextPage = soup.find_all(attrs={"rel": "next"})
print(nextPage[0]['href'])

soup.find_all(href=re.compile("elsie"), id='link1')