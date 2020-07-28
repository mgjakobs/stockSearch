import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
import datetime as dt 
import pandas as pd

#Class that extract data from yahoo finance.
#The class also contain functions for technical analysis estimates, e.g.
#global minimum, rsi, etc.
#and for plotting.

class Analyzer():
    def __init__(self):
        self.start = dt.datetime(2018,1,1)
        self.end = dt.datetime.now()

    def get_tickers_info(self):
        #tobj = yf.Tickers(self.tickersList)
        #return tobj
        pass

    def get_data(self,ticker):
        #print(ticker)
        data = yf.download(ticker, self.start, self.end)
        return data

    def global_minimum(self, data):
        state = False
        if data["Adj Close"].iloc[-1] == data["Adj Close"].min():
            state = True
        return state

    def bollingerBands(self, data):
        df = pd.DataFrame(columns = ['MA20', '20dSTD', 'upperB', 'lowerB'])

        #number of std. deviations.
        m = 2
        winSize = 20

        df['MA20'] = data['Close'].ewm(span = winSize).mean()
        df['20dSTD'] = data['Close'].ewm(span = winSize).std()
        df['upperB'] = df['MA20'] + df['20dSTD']*m
        df['lowerB'] = df['MA20'] - df['20dSTD']*m
        
        return df

    def upper_bollinger(self, data):
        state = False
        bbands = self.bollingerBands(data)

        margin = 0.01 #1%

        #is the difference (slope) of the MA20 positive or negative over 10 samples?
        diffMA20 = bbands['MA20'][-1] - bbands['MA20'][-10:].mean()

        #is the difference (slope) of the closing price positive or negatve over 10 samples?
        diffClose = data['Close'][-1] - data['Close'][-10:].mean()

        #if the slope is positive
        if (diffMA20 > 0 and diffClose > 0):
            #If the Close price has just gone up throug MA20 (uptrend)
            if (data['Close'][-1]*(1+margin) > bbands['MA20'][-1]
                and data['Close'][-1]*(1-margin) < bbands['MA20'][-1]):
                state = True

        return state

    def golden_cross(self, data):
        state = False

        df = pd.DataFrame(columns = ['MA50', 'MA200'])

        df['MA50'] = data['Close'].ewm(span = 50).mean()
        df['MA200'] = data['Close'].ewm(span = 200).mean()
        
        diffMA50 = df['MA50'][-1] - df['MA50'][-10:].mean()

        margin = 0.01 #1% margin

        if diffMA50 > 0:
            if (df['MA50'][-1]*(1+margin) > df['MA200'][-1] and 
                df['MA50'][-1]*(1-margin) < df['MA200'][-1]):
                state = True
        
        return state

    def plot_data(self, ticker, stockName, data):
        '''
        mc = mpf.make_marketcolors(
                            up='tab:green',down='tab:red',
                            edge='green',
                            wick={'up':'green','down':'red'},
                            volume='tab:green',
                           )

        s  = mpf.make_mpf_style(marketcolors=mc)
        '''

        data['MA50'] = data['Close'].ewm(span = 50).mean()
        data['MA200'] = data['Close'].ewm(span = 200).mean()

        bollingerFrame = self.bollingerBands(data)
        bbands = bollingerFrame[['MA20', 'upperB', 'lowerB']]
        
        apd = mpf.make_addplot(bbands, linestyle = 'dashed', width = 0.6, color = 'white')
        apd1 = mpf.make_addplot(data['MA50'])
        apd2 = mpf.make_addplot(data['MA200'])

        
        #Moving averages
        MA_short = 50
        MA_long = 200

        fig, ax = mpf.plot(data, title = "{} ({})".format(stockName, ticker), 
                  figscale = 2.0, type = 'candle', style = 'nightclouds', 
                  ylabel = "Price", volume = True, addplot = [apd1,apd2,apd], returnfig = True)
        
        fig.legend(['MAV{}'.format(MA_short), 'MAV{}'.format(MA_long), 'Bollinger Bands',
                    ], frameon = False)
        plt.show()
        return

