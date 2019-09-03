'''
Created on Aug 10, 2019

@author: Travis
'''

from retrieve.retriever import StockDataRetriever as analysis

if __name__ == '__main__':
    pass

class BullishAnalysis:
    
    # The body may be red or green
    # Body deviation should be no more than 2%
    # Shadow must be at least 2*Body Height
    # Returns False if the specifications are not met, True if they are met.
    def check_hammer(self, stockData):
        high = analysis.getHigh(self, stockData, 1)
        low = analysis.getLow(self, stockData, 1)
        open = analysis.getOpen(self, stockData, 1)
        close = analysis.getClose(self, stockData, 1)
             
        redStick = False
        
        if open > close:
            redStick = True
            realBodyPercent = open/close - 1
        else: # open <= close:
            realBodyPercent = close/open - 1
            
        if realBodyPercent > .02:
            return False
        
        if redStick:
            realBodyHeight = open - close
            shadowHeight = close - low
        else: # open <= close:
            realBodyHeight = close - open
            shadowHeight = open - low
        
        if shadowHeight <= 2 * realBodyHeight:
            return False
        
        return True
    def checkInverseHammer(self, stockData):
        return
    
    def checkBullishEngulfing(self, stockData):
        return
    
    def checkPiercingLine(self, stockData):
        return
    
    def checkMorningStart(self, stockData):
        return
    
    def checkThreeWhiteSoldiers(self, stockData):
        return