#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re

def removeDuplicates(xy):
  return list(dict.fromkeys(xy))
    
def getLastPage(soup):
    regex3 = r"ajaxLoad\=true\'\, true\)\"\>[0-9]+\<"
    lastpage = re.findall(regex3, str(soup))
    length = len(lastpage)
    getPageNumber = re.findall(r"[0-9]+", lastpage[length-1])
    return int(getPageNumber[0])

def choosePage(url, goToPage):
    return url + "&page=" + str(goToPage)

def getHtml(URL):
    page = requests.get(URL)
    return BeautifulSoup(page.content, "html.parser")

def getMatches(soup):
    urls = []
    matches = []
    regex = r"\/bg\/[a-z0-9A-Z\-]+\/[a-zA-Z0-9\-]+\/p/[0-9]+"
    for a in soup.find_all('a', href=True):
        urls.append(a['href'])
    for x in urls:
        m = re.findall(regex, x)
        if (m):
            matches.append(m[0])
    return matches
    
def ifPagerExists(soup):
    substring = r"paging"
    foundpager = re.findall(substring, str(soup))
    if foundpager[0] == "paging":
        return True

if __name__ == '__main__':

    matches = []

    
    URL = choosePage(1)
    soup = getHtml(URL)

    isTrue = ifPagerExists(soup)

    if isTrue:
        finalPage = int(getLastPage(soup))
        for x in range(1, finalPage + 1):
            URL2 = choosePage(x)
            soup2 = getHtml(URL2)
            matches.append(getMatches(soup2))

        links = []

        for match in matches:
            for x in match:
                links.append(x)

        links = removeDuplicates(links)

        for y in links:
            print(y)