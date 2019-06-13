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

# Aids in finding data from IEX
class Trade():
#     # Returns the nearest open market day to the end of the data set
#     @classmethod
#     def first_open_market_day(self, data, daysAgo):    
#         today = dt.datetime.now()      
#         daysAgoCounter = daysAgo
#         while (daysAgoCounter <= 0):
#             day = today + dt.timedelta(daysAgoCounter)
#             try:                
#                 return data.loc[day.strftime('%Y-%m-%d')]
#             except:
#                 daysAgoCounter += 1
#                 
#         return None
#     # Returns the nearest open market day to the beginning of the data set
#     @classmethod
#     def last_open_market_day (self, data, daysAgo):        
#         today = dt.datetime.now()      
#         daysAgoCounter = 0
#         while (daysAgoCounter >= daysAgo):
#             day = today + dt.timedelta(daysAgoCounter)
#             try:                
#                 return data.loc[day.strftime('%Y-%m-%d')]
#             except:
#                 daysAgoCounter -= 1
#                 
#         return None
#     
#     @classmethod
#     def retrieve_symbol_data(self, symbol, startDaysAgo, numberOfWeeks):
#         startDaysAgo = -1 * startDaysAgo
#         today = dt.datetime.now()
#         startDate = today + dt.timedelta(startDaysAgo)
#         endDate = today + dt.timedelta(startDaysAgo + (7 * numberOfWeeks))
#         return web.DataReader(symbol, 'iex', startDate, endDate)
#         
#     # Calculates percentage gain or loss from startDaysAgo until numberOfWeeks later.
#     # Uses closest trading days within the given parameters.
#     @classmethod
#     def buy_calc(self, data, startDaysAgo, numberOfWeeks):
#         startDaysAgo = -1 * startDaysAgo
#         endDaysAgo = startDaysAgo + (7 * numberOfWeeks)
#         endDate = dt.datetime.now() + dt.timedelta(endDaysAgo)
#         firstDay = Trade.first_open_market_day(data, startDaysAgo)
#         lastDay = Trade.last_open_market_day(data, endDaysAgo)
#         firstDayAverage = (firstDay["high"] + firstDay["low"])/2
#         lastDayAverage = (lastDay["high"] + lastDay["low"])/2
#         gain = lastDayAverage/firstDayAverage
# 
#         if gain <= 0.9:
#             print("Consider Buy")
#             gain = int(-100*(1 - gain))
#             print(str(gain) + '%')
#             infoArray = [gain, lastDayAverage, endDate]
#             return infoArray
#         elif gain > 0.9 and gain < 1:
#             print("Hold")
#             gain = int(-100*(1 - gain))
#             print(str(gain) + '%')
#             infoArray = [gain, lastDayAverage, endDate]
#             return infoArray 
#         else:
#             print("Consider Sell")
#             gain = int(gain-1)
#             print(str(gain) + '%')
#             infoArray = [gain, lastDayAverage, endDate]
#             return infoArray 
#             
#         
#     @classmethod
#     def first_day_10ROI(self, symbol, boughtDaysAgo, buyPrice):
#         boughtDaysAgo = -1 * boughtDaysAgo
#         today = dt.datetime.now()
#         startDate = today + dt.timedelta(boughtDaysAgo)
#         data = web.DataReader(symbol, 'iex', startDate, today)
#     
#         sellPrice = buyPrice + (buyPrice * 0.1)
#         print("Sell Price: " + str(sellPrice))
#         daysAgo = boughtDaysAgo
#         while (daysAgo <= 0):
#             day = today + dt.timedelta(daysAgo)
#             try:                
#                 daysHigh = data.loc[day.strftime('%Y-%m-%d')]["high"]
#                 print (daysHigh)
#                 if (daysHigh >= sellPrice):
#                     print(day.strftime('%Y-%m-%d'))
#                     print("price = " + str(daysHigh))
#                     return None
#                 else:
#                     daysAgo += 1
#             except:
#                 daysAgo += 1
                
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
        
    @classmethod
    def getStockHighs(self, data, today, dataDaysAgo):
        stockHighs = {}
        
        for highDaysAgo in range(dataDaysAgo, 0):
            dateAgo = today + dt.timedelta(highDaysAgo)
            currentHigh = Trade.getHigh(data, today, dateAgo)
            if currentHigh != None:
                stockHighs[dateAgo.strftime('%Y-%m-%d')] = currentHigh
        
        return stockHighs   
        
    @classmethod
    def getStockLows(self, data, today, dataDaysAgo):
        for lowDaysAgo in range(dataDaysAgo, 0):
            dateAgo = today + dt.timedelta(lowDaysAgo)
            currentLow = Trade.getLow(data, today, dateAgo)
            if currentLow != None:
                stockLows[dateAgo.strftime('%Y-%m-%d')] = currentLow
            
        return stockLows
    
if __name__ == '__main__':
    #style.use('ggplot')
    
    file = open("stocksRecord", "a")
    
    dataDaysAgo = -180
    today = dt.datetime.now()
    dateAgo = today + dt.timedelta(dataDaysAgo)
    
    stockLows = {}
    stockName = 'TSLA'
    data = web.DataReader(stockName, 'iex', dateAgo, today)
    
    stockHighs = Trade.getStockHighs()
    stockLows = Trade.getStockLows()
    
    for buyDaysAgo in range(dataDaysAgo, 0):
        buyDateAgo = (today + dt.timedelta(buyDaysAgo)).strftime('%Y-%m-%d')
        if buyDateAgo in stockHighs:
            buyPrice = stockHighs[buyDateAgo]
            
            for sellDaysAgo in range(buyDaysAgo, 0):
                sellDateAgo = (today + dt.timedelta(sellDaysAgo)).strftime('%Y-%m-%d')
                if sellDateAgo in stockLows:
                    sellPrice = stockLows[sellDateAgo]
                    if sellPrice >= buyPrice*1.1:
                        file.write(str(stockName) + ", " + str(buyDateAgo) + ", " + str(buyPrice) + ", " + str(sellDateAgo) + ", " + str(sellPrice) + "\n")
                        break
        
    file.close()
    #firstDay = Trade.first_open_market_day(f, daysAgo)
    #lastDay = Trade.last_open_market_day(f, daysAgo)
    #print(firstDay["open"] - lastDay["open"])
    #print(firstDay["high"] - firstDay["low"])
    
    
    
    #symbol = 'TSLA'
    #daysAgo = 30
    #numWeeks = 3
    #data = Trade.retrieve_symbol_data('TSLA', daysAgo, numWeeks)
    #buyPrice = Trade.buy_calc(data, daysAgo, numWeeks)
    #Trade.first_day_10ROI('TSLA', daysAgo - (7 * numWeeks), buyPrice)
    
        