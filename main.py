from bs4 import BeautifulSoup
import requests
import re

initialUrl = 'https://pl.dotabuff.com/players/41771279/matches?enhance=overview&page=57'
urlPrefix = 'https://pl.dotabuff.com'
matchesList = []
matchesDetails = {}

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
    print(nextPage)
    if (nextPage != None):
        #dotabuffParser(setPage(urlPrefix + nextPage))
        print('This is the last page')

def getMatchDetails(soup):
    matchDetail = {}
    direTeam = []
    radiantTeam = []
    for aElement in soup.find_all(class_=re.compile('player-dire link-type-player')):
        #matchesList.append(aElement['class'])
        direTeam.append(aElement.contents[0])
        #matchDetail[aElement.contents[0]] = "dire"

    for aElement in soup.find_all(class_=re.compile('player-radiant link-type-player')):
        #matchesList.append(aElement['class'])
        radiantTeam.append(aElement.contents[0])
        #matchDetail[aElement.contents[0]] = "radiant"
    matchDetail['dire'] = direTeam
    matchDetail['radiant'] = radiantTeam
    return matchDetail

def runMatchesLoop():
    #for match in matchesList:
    for x in range(5):

        soup = setPage(urlPrefix+matchesList[x])
        #matchID = match.split('/')[2]
        matchID = matchesList[x].split('/')[2]
        print(matchID)
        matchesDetails[matchID] = getMatchDetails(soup)

def main():
    laZuppa = setPage(initialUrl)
    dotabuffParser(laZuppa)
    runMatchesLoop()
    print(matchesDetails)


main()