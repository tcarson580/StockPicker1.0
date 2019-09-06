'''
Created on Aug 31, 2019

@author: FN-1776
'''

from retrieve.retriever import StockDataRetriever as analysis
from analysis.bullish import BullishAnalysis as bullish

def is_bullish(stockData):
    isBullish = []
    
    if bullish.is_hammer(stockData):
        isBullish.append("hammer")
    if bullish.is_inverted_hammer(stockData):
        isBullish.append("inverted hammer")
    if bullish.is_bullish_engulfing(stockData):
        isBullish.append("bullish engulfing")
    if bullish.is_morning_star(stockData):
        isBullish.append("morning star")
    if bullish.is_piercing_line(stockData):
        isBullish.append("piercing line")
    if bullish.is_three_white_soldiers(stockData):
        isBullish.append("three white soldiers")
        
    return isBullish
    
def getStockSymbols(fileName):
    file = open(fileName, "r")
    return str(file.read()).split("\n")
    
if __name__ == '__main__':
    stockNames = getStockSymbols("sp500_symbols")
    analysisFile = open("5Sept19", "w+")
    client = analysis()
    
    for stockName in stockNames:
        try:
            stockData = client.getData(stockName, '2019-08-28', '2019-09-05')
            stockDataNotToday = stockData[:-1]
            isBullish = is_bullish(stockData)
            if not isBullish:
                analysisFile.write(stockName, ",")
                for pattern in isBullish:
                    analysisFile.write(pattern, ";")
                analysisFile.write("\n")
        except:
            None
