import threading
import urllib.request
from queue import Queue
import requests
import bs4
import time
import csv
import json

response = urllib.request.urlopen('https://finance.yahoo.com/quote/afi/key-statistics')
soup = bs4.BeautifulSoup(response,"lxml")
#Remove junk data
[s.extract() for s in soup('script')]
[s.extract() for s in soup('meta')]
[s.extract() for s in soup('head')]
soup.find('div', id='masterNav').extract()
soup.find('div', id='YDC-UH').extract()
soup.find('div', id='Navigation').extract()
soup.find('div', id='YDC-Lead').extract()
soup.find('div', id='YDC-Col2').extract()



#print(soup)
try:
    pegRatioSpan = soup.findAll('span', string='PEG Ratio (5 yr expected)')[0].parent.parent
except IndexError:
    pass
else:
    pegText = pegRatioSpan.findAll('span')[0].text
    pegValue = pegRatioSpan.findAll('td')[1].text

# print(pegText)
# print(pegValue)
