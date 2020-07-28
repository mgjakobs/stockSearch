import bs4 as bs
import pickle
import requests
import sys

#This class uses webscrabing (requests + bs4) to get the stock tickers
#of popular stock index such S&P500 etc.

class Ticker():
    def __init__(self):
        return

    def saveTickersList(self, index):
        if index == 'sp500':
            self.saveSP500Tickers()
            return 'OK'

        elif index == 'c25':
            self.saveC25Tickers()

        else:
            None

    def saveSP500Tickers(self):
        resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []
        stockNames = []

        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            ticker = ticker.strip('\n')
            tickers.append(ticker)

            stockName = row.findAll('td')[1].text
            stockNames.append(stockName)
            
        with open("sp500tickers.pickle","wb") as f:
            pickle.dump([tickers, stockNames], f)
       
    def saveC25Tickers(self):
        resp = requests.get('https://en.wikipedia.org/wiki/OMX_Copenhagen_25')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find()

        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []
        stockNames = []

        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[2].text
            ticker = ticker.strip('\n')
            ticker = ticker.replace(' ', '-')
            tickers.append(ticker+'.CO')

            stockName = row.findAll('td')[0].text
            stockNames.append(stockName)
        
        with open("c25tickers.pickle","wb") as f:
            pickle.dump([tickers, stockNames], f)
