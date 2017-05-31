import threading
import urllib.request
from queue import Queue
import requests
import bs4
import time
import csv
import json

print_lock = threading.Lock()
titles = []
info = {}
def get_url(current_url):

    response = urllib.request.urlopen(current_url)
    with print_lock:
        print(response.url)

    slicin = response.url[32:len(response.url)]
    where = 0
    for char in slicin:
        if char == '/':
            break
        where += 1
    ticker = slicin[0:where]
    soup = bs4.BeautifulSoup(response,"lxml")
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('meta')]

    uhh = soup.findAll('td')
    try:
        yeah = soup.findAll('span', string='PEG Ratio (5 yr expected)')[0].parent.parent
    except IndexError:
        pass
    else:
        pegText = yeah.findAll('span')[0].text
        peg = yeah.findAll('td')[1].text
        try:
            pegFloat = float(peg)
        except ValueError:
            pass
        else:
            if peg == 'N/A':
                pass
            elif pegFloat <= 1.0 and pegFloat > 0:
                # info[temp] = {}
                # info[temp]['Industry'] = row['industry']
                info[ticker]['PEG'] = peg
                titles.append(peg)

def process_queue():
    while True:
        current_url = url_queue.get()
        get_url(current_url)
        url_queue.task_done()
url_list = []
url_queue = Queue()
words = []
with open('companylist.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    #count = 0
    for row in reader:
        temp = row['Symbol']
        if temp.isalpha():
            words.append(temp)
            info[temp] = {}
            info[temp]['Industry'] = row['industry']
            info[temp]['PEG'] = 'balls'
            #count +=1
            # if count > 50:
            #     break

#words = ["AAPL", "GOOG", "YHOO", "AMD", "MSFT"]
for word in words:
    url_list.append('https://finance.yahoo.com/quote/' + word + '/key-statistics')

for i in range(30):
    t = threading.Thread(target=process_queue)
    t.daemon = True
    t.start()

start = time.time()

for current_url in url_list:
    url_queue.put(current_url)

url_queue.join()

#print(threading.enumerate())
delete = []
#print("Execution time = {0:.5f}".format(time.time() - start))
for item in info:
    if info[item]['PEG'] != 'balls':
        print('Company: ' + item)
        print('PEG: ' + info[item]['PEG'])
        print('Industry: ' + info[item]['Industry'])
    else:
        delete.append(item)
for item in delete:
    del info[item]

with open('data.txt', 'w') as outfile:
    json.dump(info, outfile)
