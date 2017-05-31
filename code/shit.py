import urllib.request
from bs4 import BeautifulSoup
import lxml
import csv

name = []
info = {}

with open('companylist.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    #count = 0
    for row in reader:
        temp = row['Symbol']
        if temp.isalpha():

            response = urllib.request.urlopen('https://finance.yahoo.com/quote/' + temp + '/key-statistics')
            print(response.url)
            soup = BeautifulSoup(response, "lxml")
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
                    elif pegFloat <= 1.2:
                        info[temp] = {}
                        info[temp]['Industry'] = row['industry']
                        info[temp]['PEG'] = peg


            # count += 1
            # if count > 3:
            #     break


for item in info:
    print('Company: ' + item)
    print('PEG: ' + info[item]['PEG'])
    print('Industry: ' + info[item]['Industry'])



# response = urllib.request.urlopen('https://finance.yahoo.com/quote/' + name[0] + '/key-statistics')
# soup = BeautifulSoup(response, "lxml")
# [s.extract() for s in soup('script')]
# [s.extract() for s in soup('meta')]
#
# uhh = soup.findAll('td')
#
#
#
# yeah = soup.findAll('span', string='PEG Ratio (5 yr expected)')[0].parent.parent
#
# pegText = yeah.findAll('span')[0].text
# peg = yeah.findAll('td')[1].text
