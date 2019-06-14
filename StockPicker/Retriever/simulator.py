'''
Created on Jun 13, 2019

@author: Travis
'''
import datetime as dt
import time

class simulator():
    '''
    classdocs
    '''
        
    @classmethod    
    def getStockData(self, fileName):
        stockData = {}
        file = open(fileName, "r")
        buyStocks = str(file.read()).splitlines()
        i = 0
        while i < len(buyStocks):
            stockData[str(i)] = list(map(str, buyStocks[i].split(",")))
            i += 1
    
        return stockData
    
    @classmethod    
    def buyStock(self, stockData, stockList, quantity):
        stockData.append(quantity)
        stockList[stockData[0]] = stockData
        return stockList
    
    
    
    @classmethod
    def sellStock(self):
        None
        
if __name__ == '__main__':
    t0 = time.time()
    
    startingCapital = 1000.00
    investableCapital = startingCapital
    maxPurchase = 0.05*startingCapital
    
    dataDaysAgo = -360
    today = dt.datetime.now()
    dateAgo = today + dt.timedelta(dataDaysAgo)
    
    stockData = simulator.getStockData("stocksRecord")
    itemsToSell = []
    currentHeldStocks = {}
    
    for date in range(dataDaysAgo, 0):
        currentDate = (today + dt.timedelta(date)).strftime('%Y-%m-%d')
        
        # Buy stocks at beginning of day
        for number, stock in stockData.items():
            stockName = stock[0]
            buyDate = stock[1]
            buyPrice = float(stock[2])
            if currentDate == buyDate:
                if stock[0] not in currentHeldStocks:
                    # Buy quantity no greater than max purchase or current capital, whichever is lower
                    quantity = int(min(maxPurchase/buyPrice, investableCapital/buyPrice))
                    if quantity > 0:
                        investableCapital -= round((buyPrice*quantity), 2)
                        currentHeldStocks = simulator.buyStock(stock, currentHeldStocks, quantity)

        # Record all items to sell
        for stockName, stock in currentHeldStocks.items():
            stockName = stock[0]
            sellDate = stock[3]
            sellPrice = float(stock[4])
            quantity = stock[5]
            
            if currentDate == sellDate:
                itemsToSell.append(stockName)
                investableCapital += round((sellPrice*quantity), 2)
               
        # Sell items; 
        # can't remove items from dictionary in previous for loop due to runtime error
        for stockName in itemsToSell:
            del currentHeldStocks[stockName]
            
        itemsToSell.clear()
        print("Date: ", currentDate) 
        print("Money ready to invest: $", round(investableCapital, 2))    
            
    print("Last Date in Simulation: ", currentDate) 
    print("Initial investment: $", round(startingCapital, 2))    
    print("Capital at end of simulation: $", round(investableCapital, 2))          
    t1 = time.time()           
    total = t1-t0
    #print(total, "seconds")            
                