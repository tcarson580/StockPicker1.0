'''
Created on Apr 21, 2019

@author: Travis
'''
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import array
import time

# Aids in finding data from IEX
class Trade():
    @classmethod    
    def getStockSymbols(self, fileName):
        file = open(fileName, "r")
        return str(file.read()).split(",")
          
    # Returns stock high for the day, or None if no data exists
    @classmethod
    def getHigh(self, data, today, dateAgo):
        try:                
            return data.loc[dateAgo.strftime('%Y-%m-%d')]['high']
        except:
            return None  
        
    # Returns stock low for the day, or None if no data exists
    @classmethod
    def getLow(self, data, today, dateAgo):
        try:                
            return data.loc[dateAgo.strftime('%Y-%m-%d')]['low']
        except:
            return None  
    
    # Returns hash table of all valid stock highs between the specified days ago and today    
    @classmethod
    def getStockHighs(self, data, today, dataDaysAgo):
        stockHighs = {}
        print("starting stock highs")
        for highDaysAgo in range(dataDaysAgo, 0):
            dateAgo = today + dt.timedelta(highDaysAgo)
            currentHigh = Trade.getHigh(data, today, dateAgo)
            if currentHigh != None:
                print(currentHigh)
                stockHighs[dateAgo.strftime('%Y-%m-%d')] = currentHigh
                print(stockHighs[dateAgo.strftime('%Y-%m-%d')])
        
        return stockHighs   
    
    # Returns hash table of all valid stock lows between the specified days ago and today       
    @classmethod
    def getStockLows(self, data, today, dataDaysAgo):
        stockLows = {}
        
        for lowDaysAgo in range(dataDaysAgo, 0):
            dateAgo = today + dt.timedelta(lowDaysAgo)
            currentLow = Trade.getLow(data, today, dateAgo)
            if currentLow != None:
                stockLows[dateAgo.strftime('%Y-%m-%d')] = currentLow
            
        return stockLows
    
    @classmethod
    def calculateBuySellDates(self, data, today, dataDaysAgo, stockName, stockHighs, stockLows):
        file = open("stocksRecord", "a")
        
        minimumProfit = 1.1 #10% ROI
        
        for buyDaysAgo in range(dataDaysAgo, 0):
            buyDateAgo = (today + dt.timedelta(buyDaysAgo)).strftime('%Y-%m-%d')
            if buyDateAgo in stockHighs:
                buyPrice = stockHighs[buyDateAgo]
                
                for sellDaysAgo in range(buyDaysAgo, (buyDaysAgo+31)):
                    sellDateAgo = (today + dt.timedelta(sellDaysAgo)).strftime('%Y-%m-%d')
                    if sellDateAgo in stockLows:
                        sellPrice = stockLows[sellDateAgo]
                        if sellPrice >= buyPrice * minimumProfit:
                            file.write(str(stockName) + "," + str(buyDateAgo) + "," + str(buyPrice) + "," + str(sellDateAgo) + "," + str(sellPrice) + "\n")
                            break
        file.close()    
                   
if __name__ == '__main__':
    #style.use('ggplot')
    t0 = time.time()
    file = open("stocksRecord", "w").close()
    
    dataDaysAgo = -720
    today = dt.datetime.now()
    dateAgo = today + dt.timedelta(dataDaysAgo)
    
    stockNames = Trade().getStockSymbols("sp500_symbols")
    
    for stockName in stockNames:
        try:
            data = web.DataReader(stockName, 'IEX_SANDBOX', dateAgo, today)
            stockHighs = Trade.getStockHighs(data, today, dataDaysAgo) 
            stockLows = Trade.getStockLows(data, today, dataDaysAgo)
            Trade().calculateBuySellDates(data, today, dataDaysAgo, stockName, stockHighs, stockLows)
        except:
            None

    t1 = time.time()
    total = t1-t0
    print(total, "seconds")

    
        