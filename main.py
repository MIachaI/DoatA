from bs4 import BeautifulSoup
import requests
import re

initialUrl = 'https://pl.dotabuff.com/players/41771279/matches?enhance=overview&page=57'
urlPrefix = 'https://pl.dotabuff.com'
matchesList = []

def setPage(url):
    r = requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"})
    return BeautifulSoup(r.text, 'html.parser')

def getMatches(soup):
    for a in soup.find_all(href=re.compile('.matches\/\d*')):
        matchesList.append(a['href'])

def getNextPage(soup):
    nextPage = soup.find_all(attrs={"rel": "next"})
    if(len(nextPage)!=0):
        return nextPage[0]['href']
    else:
        return None

def dotabuffParser(soup):
    getMatches(soup)
    nextPage = getNextPage(soup)
    if (nextPage != None):
        dotabuffParser(setPage(urlPrefix + nextPage))
        print('This is the last page')

def main():
    laZuppa = setPage(initialUrl)
    dotabuffParser(laZuppa)
    print(len(matchesList))


main()