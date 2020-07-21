from tickerGenerator import Ticker
from technicalAnalysis import Analyzer
import pickle
import sys
from os import path
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search stock index.')
    parser.add_argument('-i', '--index', help='index to be scanned (sp500, c25, dax)')
    args = parser.parse_args()

    if not args.index:
        print('You must input an index')
        sys.exit()
    
    index = args.index
    index = index.lower()
    
    tickers = Ticker()
    TA = Analyzer()

    file_name = str(index) + 'tickers.pickle'
    if not path.exists(file_name):
        resp = tickers.saveTickersList(index)
        print('Saving tickers and stocknames from {}'.format(index))
        if resp == None:
            print('Index \"{}\" is not known.'.format(index))
            sys.exit()

    with open(index+'tickers.pickle', 'rb') as f:
            tickersList, stockNameList = pickle.load(f)

    #Here starts the search flow
    for ticker, stockName in zip(tickersList, stockNameList):
        try:
            data = TA.get_data(ticker)
            if TA.global_minimum(data):
                print("Interesting stock! {}".format(ticker))
                TA.plot_data(ticker, stockName, data)
            elif TA.below_bollinger(data):
                TA.plot_data(ticker, stockName, data)
        
        except KeyboardInterrupt:
            print("\nExiting...\n")
            sys.exit()

        except Exception as e:
            print(e)
            pass
