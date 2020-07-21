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
        self.start = dt.datetime(2019,1,1)
        self.end = dt.datetime.now()

    def get_tickers_info(self):
        #tobj = yf.Tickers(self.tickersList)
        #return tobj
        pass

    def get_data(self,ticker):
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

        df['MA20'] = data['Adj Close'].rolling(window = 20).mean()
        df['20dSTD'] = data['Adj Close'].rolling(window = 20).std()
        df['upperB'] = df['MA20'] + df['20dSTD']*m
        df['lowerB'] = df['MA20'] - df['20dSTD']*m
        
        return df

    def below_bollinger(self, data):
        state = False
        bbands = self.bollingerBands(data)
        
        if data['Adj Close'].iloc[-1] < bbands['lowerB'].iloc[-1]:
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
        bollingerFrame = self.bollingerBands(data)
        bbands = bollingerFrame[['upperB', 'lowerB']]
        
        apd = mpf.make_addplot(bbands, linestyle = 'dashed', width = 0.6, color = 'white')

        fig, ax = mpf.plot(data, title = "{} ({})".format(stockName, ticker), figscale = 2.0, type = 'candle', style = 'nightclouds', ylabel = "Price", volume = True, mav = (12,24), addplot = apd, returnfig = True)
        fig.legend(['MAV12', 'MAV24', 'Upper Bollinger', 'Lower Bollinger'], frameon = False)
        plt.show()
        return

