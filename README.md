# stockSearch

Require packages: bs4, pickle, requests, sys, os, yfinance, matplotlib, mplfinance, datetime, pandas.

This repository contain python scripts to search for stocks in indexes such as sp500, etc.
Stock tickers and names are found by webscrabing e.g. wikipedia using tickerGenerator.py
Search criteria can be set via technical indicator functions defined in technicalAnalysis.py and
searchStocks.py shows an example of using tickerGenerator.py and technicalAnalysis.py.

## Examples

### Example 1
To search for stocks in sp500:
python3 searchStocks.py search -i sp500

### Example 2
Instead of searching through an index, you can plot the pricings for a particular stock in a particular index by:
python3 searchStocks.py plot -i sp500 -s INTC 
