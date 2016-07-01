# wordscrape
Search for words in Google search results

### Usage

`python3 wordscrape.py keywordfile targetfile [-h] [--delay DELAY]`

keywordfile: a text file with queries for google, one query on each line

targetfile: a text file with words to search for within the google search results, with one word on each line

DELAY: an integer for the average delay between each search, in seconds. default is 30



### Dependencies

Python 3

beautifulsoup4

selenium


### Example
An example, searching for the words in `targets.txt` on the google results pages for the queries in `keywords.txt`, with an average delay of 35 seconds:


`python3 wordscrape.py keywords.txt targets.txt --delay 35`

Example results in example/ScrapeResult.csv
