from bs4 import BeautifulSoup
import requests
import time



def soup_Scrape():
    tables = []
    body = []
    ticker = 'AMD'

    page = requests.get('https://ca.finance.yahoo.com/q/ecn?s='+ticker)
    soup = BeautifulSoup(page.text , "lxml")


    for tr in soup.find_all('table')[1:]:
        tables.append(tr.find_all('th', limit=2))
        body.append(tr.find_all('tbody', limit=2))
        
    print (tables, "\n \n \n", body,  "\n \n \n")



def timer(method):

    t0 = time.clock()

    method()

    t1 = time.clock()

    total = t1 - t0

    print ("\n\n\n", total)




#timer(soup_Scrape)         #legacy code used to see how fast lxml was,avg.34sec
