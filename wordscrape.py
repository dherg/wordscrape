# Input:
#       -.txt file with keywords to search on google (newline separated)
#       -.txt file with target words 
#           (words we are looking for on the results page) (newline separated)

# TODO:
#       - read from csv?
#       - close files after done writing
#       - clean up code
import requests
from bs4 import BeautifulSoup
import re
import csv
import random
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



def randomua():

    # from https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
    useragents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    ]

    return(random.choice(useragents))


def googlesearch(query):

    # requests version                                                                                                                                                                     
    # link = 'http://www.google.com/search?q={}'.format(query)                                                                                                                          
    # ua = {'User-Agent': randomua()}                                                                                                                                                                                                                                            
    # response = requests.get(link, headers=ua)                                                                                                                                                
    # return(response.text)

    # selenium version
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = randomua()
    driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true'])
    driver.set_window_size(1120, 550)
    driver.get('http://www.google.com/search?q={}'.format(query))
    with open('response.txt', 'w') as file:
        file.write(driver.page_source)
    pagesource = driver.page_source
    driver.quit()
    return(pagesource)

def getkeywords():
    keywords = []
    keywordsfile = open('keywords.txt', 'r')
    for line in keywordsfile:
        keywords.append(line[:-1]) # strips \n at end of term
    return(keywords)

def getresults(query):
    print('sending request for {}'.format(query))
    soup = BeautifulSoup(googlesearch(query), 'html.parser')
    print('parsing response')
    response_st = soup.find_all('span', {'class' : 'st'})
    response_r = soup.find_all('h3', {'class' : 'r'})
    regex = r'<.*?>'
    descriptions = []
    for description in response_st:
        descriptions.append(re.sub(regex, ' ', str(description)))
    links = []
    for link in response_r:
        links.append(re.sub(regex, ' ', str(link)))
    alltext = descriptions
    alltext.extend(links)
    alltext = ' '.join(alltext).lower()
    return(alltext)

def searchtargets(targets, alltext, resultsfilewriter):
    print('searching for target words')
    targetfound = []
    for target in targets:
        lowertarget = target.lower()
        if lowertarget in alltext:
            targetfound.append("True")
        else:
            targetfound.append("False")
    return(targetfound)

def main():
    keywords = getkeywords()
    targets = [line.rstrip('\n') for line in open('targets.txt', 'r')]

    # open csv file and print header line
    resultsfile = open('ScrapeResults.csv', 'w', encoding='utf8', newline='')
    resultsfilewriter = csv.writer(resultsfile, quoting=csv.QUOTE_ALL)
    header = ['Keywords']
    for target in targets:
        header.append(target)
    # print(header)
    resultsfilewriter.writerow(header)
    resultsfile.flush()

    for keyword in keywords:
        alltext = getresults(keyword)
        searchresult = searchtargets(targets, alltext, resultsfile)
        # print(searchresult)
        # print(keyword)
        row = [keyword]
        # print(row)
        row.extend(searchresult)
        # print(row)
        resultsfilewriter.writerow(row)
        resultsfile.flush()
        if keyword != keywords[len(keywords) - 1]:
            randint = random.randint(20,40)
            print('sleeping {} seconds...'.format(randint))
            time.sleep(randint)

    print('finished')
    
    



if __name__ == '__main__':
    main()
