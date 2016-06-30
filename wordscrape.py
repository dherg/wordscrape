# Input:
#		-.txt file with keywords to search on google (newline separated)
#		-.txt file with target words 
#			(words we are looking for on the results page) (newline separated)

# TODO:
#		- better output format 
#		- read from csv?
#		- 
import requests
from bs4 import BeautifulSoup
import re


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

def googlesearch(searchfor):                                                                                                                                                                                       
    link = 'http://www.google.com/search?q={}'.format(searchfor)
    # print(link)                                                                                                                            
    ua = {'User-Agent': useragents[0]}                                                                
    # payload = {'q': searchfor}                                                                                                                                                                                     
    response = requests.get(link, headers=ua)
    # with open('response.txt', 'w+') as responsefile:
    #	responsefile.write(response.text)                                                                                                                                                   
    return(response.text)

def getkeywords():
	keywords = []
	keywordsfile = open('keywords.txt', 'r')
	for line in keywordsfile:
		keywords.append(line[:-1]) # strips \n at end of term
	return(keywords)

def main():
	keywords = getkeywords()
	print('sending request for {}'.format(keywords[0]))
	soup = BeautifulSoup(googlesearch(keywords[0]), 'html.parser')
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
	print('searching for target words')
	targets = [line.rstrip('\n') for line in open('targets.txt', 'r')]

	for target in targets:
		lowertarget = target.lower()
		if lowertarget in alltext:
			print('{} - {}'.format(target, True))
		else:
			print('{} - {}'.format(target, False))
		



	with open('response.txt', 'r+') as responsefile:
		# responsefile.write(soup.prettify())
		pass








if __name__ == '__main__':
	main()
