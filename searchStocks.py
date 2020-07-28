from tickerGenerator import Ticker
from technicalAnalysis import Analyzer
import pickle
import sys
from os import path
import argparse

if __name__ == "__main__":
    #Setting up parser, reading input
    parser = argparse.ArgumentParser(description='Search stock index.')
    parser.add_argument('type', choices = ['search', 'plot'])
    parser.add_argument('-i', '--index', help='index to be scanned (sp500, c25, dax)')
    parser.add_argument('-s', '--stock', help='Stock to be plotted')
    args = parser.parse_args()

    if not args.index:
        print('You must input an index')
        sys.exit()
    
    index = args.index
    index = index.lower()
    
    #Instances of Ticker and Analyzer
    tickers = Ticker()
    TA = Analyzer()

    #Get tickers and stock names found in index.
    file_name = str(index) + 'tickers.pickle'
    if not path.exists(file_name):
        try:
            resp = tickers.saveTickersList(index)
            print('Saving tickers and stocknames from {}'.format(index))
        except resp == None:
            print('Index \"{}\" is not known.'.format(index))
            sys.exit()

    with open(index+'tickers.pickle', 'rb') as f:
            tickersList, stockNameList = pickle.load(f)

    #Flow if plotting
    if args.type == 'plot':
        if args.stock in tickersList:
            lookUp = tickersList.index(args.stock)
            print(lookUp)
            stockName = stockNameList[lookUp]
            data = TA.get_data(args.stock)
            TA.plot_data(args.stock, stockName, data)
        else:
            print("Type a stock from the tickers list\n")
            print('\n'.join('{}: {}'.format(*k) for k in enumerate(tickersList)))

    #Flow if searching
    elif args.type == 'search':
        for ticker, stockName in zip(tickersList, stockNameList):
            try:
                data = TA.get_data(ticker)

                #Set technical indicators to be used in the search.
                if TA.global_minimum(data):
                    print("Global minimum found in {}".format(ticker))
                    TA.plot_data(ticker, stockName, data)
                elif TA.upper_bollinger(data):
                    print("Bollinger uptrend in {}".format(ticker))
                    TA.plot_data(ticker, stockName, data)
                elif TA.golden_cross(data):
                    print("Golden cross uptrend in {}".format(ticker))
                    TA.plot_data(ticker, stockName, data)
            
            except KeyboardInterrupt:
                print("\nExiting...\n")
                sys.exit()

            except Exception as e:
                print(e)
                pass
    else:
        print("Exiting...")
