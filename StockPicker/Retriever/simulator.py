'''
Created on Jun 13, 2019

@author: Travis
'''
import datetime as dt
import time
import pandas_datareader.data as web

class simulator:
    '''
    classdocs
    ''' 
    def __init__(self, maxPurchasePercentage, startingCapital, dataDaysAgo):
        self.maxPurchasePercentage = maxPurchasePercentage
        self.startingCapital = startingCapital
        self.investableCapital = startingCapital
        self.currentNetWorth = startingCapital
     
        self.dataDaysAgo = -1*dataDaysAgo
        self.today = dt.datetime.now()
        self.dateAgo = self.today + dt.timedelta(dataDaysAgo)
         
        self.getStockData("stocksRecord")
        self.itemsToSell = []
        self.currentHeldStocks = {}
        self.allStockData = {}
        
    @classmethod    
    def getStockData(self, fileName):
        stockData = {}
        file = open(fileName, "r")
        buyStocks = str(file.read()).splitlines()
        i = 0
        while i < len(buyStocks):
            stockData[str(i)] = list(map(str, buyStocks[i].split(",")))
            i += 1
    
        self.stockData = stockData
        return stockData
    
    @classmethod    
    def buyStock(self, stockData, stockList, quantity):
        stockData.append(quantity)
        stockList[stockData[0]] = stockData
        return stockList
    
    @classmethod
    def sellStock(self):
        None
    
    def runSimulation(self):
        print(self.dataDaysAgo)
        currentDate = self.today    
        for date in range(self.dataDaysAgo, 0):
            currentDate = (self.today + dt.timedelta(date)).strftime('%Y-%m-%d')
            maxPurchase = self.maxPurchasePercentage*self.currentNetWorth
            
            # Buy stocks at beginning of day
            for number, stock in self.stockData.items():
                stockName = stock[0]
                buyDate = stock[1]
                buyPrice = float(stock[2])
                if currentDate == buyDate:
                    if stock[0] not in self.currentHeldStocks:
                        # Buy quantity no greater than max purchase or current capital, whichever is lower
                        quantity = int(min(maxPurchase/buyPrice, self.investableCapital/buyPrice))
                        if quantity > 0:
                            self.investableCapital -= round((buyPrice*quantity), 2)
                            self.currentHeldStocks = simulator.buyStock(stock, self.currentHeldStocks, quantity)
                            
                    # Add all stock data to dictionary from purchase date until today
                    if stock[0] not in self.allStockData:
                        print("stock[0]: ", stock[0])
                        print("currentDate: ", currentDate)
                        print("today: ", self.today)
                        self.allStockData[stock[0]] = web.DataReader(stock[0], 'iex', currentDate, self.today)
                            
    
            # Record all items to sell
            for stockName, stock in self.currentHeldStocks.items():
                stockName = stock[0]
                sellDate = stock[3]
                sellPrice = float(stock[4])
                quantity = stock[5]
                
                if currentDate == sellDate:
                    self.itemsToSell.append(stockName)
                    self.investableCapital += round((sellPrice*quantity), 2)
                   
            # Sell items; 
            # can't remove items from dictionary in previous for loop due to runtime error
            for stockName in self.itemsToSell:
                del self.currentHeldStocks[stockName]
            
            self.itemsToSell.clear()
            
            # Calculate current net worth to determine maximum purchase of any particular stock
            currentNetWorth = self.investableCapital
            tradingDay = True
            
            # Calculate net worth based on investable capital and currently held stocks' low for the day
            for stockName, stock in self.currentHeldStocks.items():
                try: 
                    self.currentNetWorth += float(self.allStockData[stock[0]].loc[currentDate]['low'])
                except:
                    tradingDay = False
             
            if tradingDay:
                print("----------------------------------------") 
                print("Date: ", currentDate) 
                print("Net Worth: $", round(self.currentNetWorth, 2))
         
        print("Last Date in Simulation: ", currentDate) 
        print("Initial investment: $", round(self.startingCapital, 2))    
        print("Capital at end of simulation: $", round(self.investableCapital, 2))   
if __name__ == '__main__':
    t0 = time.time()
    
    simulator = simulator(0.05, 1000.00, 360)
    simulator.runSimulation()
    
    
#     maxPurchasePercentage = 0.05
#     startingCapital = 1000.00
#     investableCapital = startingCapital
#     currentNetWorth = startingCapital
#     maxPurchase = maxPurchasePercentage*startingCapital
#       
#     dataDaysAgo = -360
#     today = dt.datetime.now()
#     dateAgo = today + dt.timedelta(dataDaysAgo)
#       
#     stockData = simulator.getStockData("stocksRecord")
#     itemsToSell = []
#     currentHeldStocks = {}
#     allStockData = {}
#       
#     for date in range(dataDaysAgo, 0):
#         currentDate = (today + dt.timedelta(date)).strftime('%Y-%m-%d')
#         maxPurchase = maxPurchasePercentage*currentNetWorth
#           
#         # Buy stocks at beginning of day
#         for number, stock in stockData.items():
#             stockName = stock[0]
#             buyDate = stock[1]
#             buyPrice = float(stock[2])
#             if currentDate == buyDate:
#                 if stock[0] not in currentHeldStocks:
#                     # Buy quantity no greater than max purchase or current capital, whichever is lower
#                     quantity = int(min(maxPurchase/buyPrice, investableCapital/buyPrice))
#                     if quantity > 0:
#                         investableCapital -= round((buyPrice*quantity), 2)
#                         currentHeldStocks = simulator.buyStock(stock, currentHeldStocks, quantity)
#                           
#                 # Add all stock data to dictionary from purchase date until today
#                 if stock[0] not in allStockData:
#                     allStockData[stock[0]] = web.DataReader(stock[0], 'iex', currentDate, today)
#                           
#   
#         # Record all items to sell
#         for stockName, stock in currentHeldStocks.items():
#             stockName = stock[0]
#             sellDate = stock[3]
#             sellPrice = float(stock[4])
#             quantity = stock[5]
#               
#             if currentDate == sellDate:
#                 itemsToSell.append(stockName)
#                 investableCapital += round((sellPrice*quantity), 2)
#                  
#         # Sell items; 
#         # can't remove items from dictionary in previous for loop due to runtime error
#         for stockName in itemsToSell:
#             del currentHeldStocks[stockName]
#           
#         itemsToSell.clear()
#           
#         # Calculate current net worth to determine maximum purchase of any particular stock
#         currentNetWorth = investableCapital
#         tradingDay = True
#           
#         # Calculate net worth based on investable capital and currently held stocks' low for the day
#         for stockName, stock in currentHeldStocks.items():
#             try: 
#                 currentNetWorth += float(allStockData[stock[0]].loc[currentDate]['low'])
#             except:
#                 tradingDay = False
#            
#         if tradingDay:
#             print("----------------------------------------") 
#             print("Date: ", currentDate) 
#             print("Net Worth: $", round(currentNetWorth, 2))
#           
#           
#               
#     print("Last Date in Simulation: ", currentDate) 
#     print("Initial investment: $", round(startingCapital, 2))    
#     print("Capital at end of simulation: $", round(investableCapital, 2))          
    t1 = time.time()           
    total = t1-t0
    print(total, "seconds")            
                