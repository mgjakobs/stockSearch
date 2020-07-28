# stockSearch

This repository contain python scripts to search for stocks in indexes such as sp500, etc.

Stock tickers and names are found by webscrabing e.g. wikipedia using tickerGenerator.py

Search criteria can be set via technical indicator functions defined in technicalAnalysis.py

searchStocks.py shows an example of using tickerGenerator.py and technicalAnalysis.py.

Example
python3 searchStocks.py -i sp500
