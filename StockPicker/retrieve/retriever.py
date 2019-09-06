'''
Created on Aug 10, 2019

@author: Travis
'''
from tiingo import TiingoClient

class StockDataRetriever:
    client = ""
    
    def __init__(self):
        config = {}
        config['session'] = True
        config['api_key'] = "b061027e46f532a4cfb0e91a9ff444a0582302cc"
        self.client = TiingoClient(config)
    
    def getData(self, symbol, startDate, endDate):
#         return self.client.get_ticker_price(symbol, fmt, startDate, endDate, frequency)
        return self.client.get_ticker_price(symbol,
                                       fmt='json',
                                       startDate=startDate,
                                       endDate=endDate,
                                       frequency='daily')
    
    @staticmethod
    def getHigh(stockData, daysAgo):
        daysAgo = -1*daysAgo   
        return stockData[daysAgo].get('high')
    
    @staticmethod
    def getLow(stockData, daysAgo):
        daysAgo = -1*daysAgo    
        return stockData[daysAgo].get('low')
    
    @staticmethod
    def getOpen(stockData, daysAgo):
        daysAgo = -1*daysAgo    
        return stockData[daysAgo].get('open')
    
    @staticmethod
    def getClose(stockData, daysAgo):
        daysAgo = -1*daysAgo    
        return stockData[daysAgo].get('close')
    
    
if __name__ == '__main__':
    client = StockDataRetriever()
    print(client.getData("TSLA", '2019-08-19', '2019-08-023'))