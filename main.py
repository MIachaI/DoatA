from bs4 import BeautifulSoup
import requests
import re

url = 'https://pl.dotabuff.com/players/41771279/matches'
matchesList = []
r = requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"})

soup = BeautifulSoup(r.text, 'html.parser')

for a in soup.find_all('a', href=True):
    if(re.findall('.matches\/\d*',a['href'])):
        matchesList.append(a['href'])

#print(soup.find_all('a rel'))
print(matchesList)

