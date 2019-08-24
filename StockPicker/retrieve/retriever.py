'''
Created on Aug 10, 2019

@author: Travis
'''

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import array
import time

if __name__ == '__main__':
    dataDaysAgo = -2
    today = dt.datetime.now()
    dateAgo = today + dt.timedelta(dataDaysAgo)
    stockName = 'TSLA'
    data = web.DataReader(stockName, 'iex', dateAgo, today)

#class StockDataRetriever:
    