# Input:
#		-.txt file with keywords to search on google (newline separated)
#		-.txt file with target words 
#			(words we are looking for on the results page) (newline separated)

keywords = []

def getkeywords():
	keywordsfile = open('keywords.txt', 'r')
	for line in keywordsfile:
		keywords.append(line[:-1]) # strips \n at end of term

def main():
	getkeywords()
	print(keywords)






if __name__ == '__main__':
	main()
