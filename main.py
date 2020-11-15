from bs4 import BeautifulSoup
import requests
import re
from dict2xml import dict2xml 
from collections import Counter

initialUrl = 'https://pl.dotabuff.com/players/41771279/matches?enhance=overview&page=57'
urlPrefix = 'https://pl.dotabuff.com'
matchesList = []
matchesDetails = {}
enemiesList = []

def setPage(url):
    r = requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"})
    return BeautifulSoup(r.text, 'html.parser')

def getMatches(soup):
    for a in soup.find_all(href=re.compile('.matches\/\d*'), class_=re.compile('.*')):
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
    #print(nextPage)
    if (nextPage != None):
        #dotabuffParser(setPage(urlPrefix + nextPage))
        print('This is the last page')

def getMatchDetails(soup):
    matchDetail = {}
    direTeam = []
    radiantTeam = []
    for aElement in soup.find_all(class_=re.compile('player-dire link-type-player')):
        direTeam.append(aElement.contents[0])

    for aElement in soup.find_all(class_=re.compile('player-radiant link-type-player')):
        radiantTeam.append(aElement.contents[0])

    matchDetail['dire'] = direTeam
    matchDetail['radiant'] = radiantTeam

    return matchDetail

def runMatchesLoop():
    for match in matchesList:
        soup = setPage(urlPrefix+match)
        matchID = match.split('/')[2]
        print(matchID)
        matchesDetails[matchID] = getMatchDetails(soup)

def analyzeMatches():
    for match in matchesDetails.values():
        if 'MIachaI' in match['dire']:
            for x in match['radiant']:
                enemiesList.append(x)
        else:
            for x in match['dire']:
                enemiesList.append(x)

def saveDictToXmlFile():
    xml = dict2xml(matchesDetails)
    text_file = open("RawXML.txt", "w")
    text_file.write(xml)
    text_file.close()

    xml2 = dict2xml(Counter(enemiesList))
    text_file = open("CountedEnemies.txt", "w")
    text_file.write(xml2)
    text_file.close()

def main():
    laZuppa = setPage(initialUrl)
    dotabuffParser(laZuppa)
    runMatchesLoop()

    analyzeMatches()
    saveDictToXmlFile()


main()