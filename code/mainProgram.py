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

    slicinForTick = response.url[32:len(response.url)]
    stopPos = 0
    for char in slicinForTick:
        if char == '/':
            break
        stopPos += 1
    ticker = slicinForTick[0:stopPos]
    soup = bs4.BeautifulSoup(response,"lxml")
    #Remove junk data
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('meta')]


    try:
        pegRatioSpan = soup.findAll('span', string='PEG Ratio (5 yr expected)')[0].parent.parent
    except IndexError:
        pass
    else:
        pegText = pegRatioSpan.findAll('span')[0].text
        pegValue = pegRatioSpan.findAll('td')[1].text
        try:
            pegFloat = float(pegValue)
        except ValueError:
            pass
        else:
            if pegValue == 'N/A':
                pass
            elif pegFloat <= 1.0 and pegFloat > 0:
                info[ticker]['PEG'] = pegValue

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
            # count +=1
            # if count > 50:
            #     break

for word in words:
    url_list.append('https://finance.yahoo.com/quote/' + word + '/key-statistics')

#determine how many threads to make
for i in range(10):
    t = threading.Thread(target=process_queue)
    t.daemon = True
    t.start()

start = time.time()

for current_url in url_list:
    url_queue.put(current_url)

url_queue.join()

delete = []
#only print companies that have a proper PEG value
print('Completed retrieval, parsing...')

for item in info:
    if info[item]['PEG'] != 'balls':
        # print('Company: ' + item)
        # print('PEG: ' + info[item]['PEG'])
        # print('Industry: ' + info[item]['Industry'])
        pass
    else:
        delete.append(item)
for item in delete:
    del info[item]

print('Completed parsing, writing to file...')

with open('data.txt', 'w') as outfile:
    json.dump(info, outfile)

print('Completed')
print(str(time.time() - start) + ' seconds')
