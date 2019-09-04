'''
Created on Aug 10, 2019

@author: Travis
'''

from retrieve.retriever import StockDataRetriever as analysis

if __name__ == '__main__':
    pass

#Terminology:
    # Shadow = upper wick
    # Tail = lower wick
    # Red Stick = Close was lower than open
        # Do not use body, as redBody can be confused with realBody
    # Green Stick = Close was higher than open
    # Real Body = difference between open and close

class BullishAnalysis:
    
    # The body may be red or green
    # Body deviation should be no more than 2%
    # Tail must be at least 2*Body Height
    # Shadow must be within 1 real body height of the open/close (whichever is higher)
    # Returns False if the specifications are not met, True if they are met.
    def is_hammer(self, stockData):
        try:
            high = analysis.getHigh(self, stockData, 1)
            low = analysis.getLow(self, stockData, 1)
            open = analysis.getOpen(self, stockData, 1)
            close = analysis.getClose(self, stockData, 1)
        except:
            return False
             
        redStick = False
        
        # Check body deviation
        if open > close:
            redStick = True
            realBodyPercent = open/close - 1
        else: # open <= close:
            realBodyPercent = close/open - 1
            
        if realBodyPercent > .02:
            return False
        
        # Check shadow and tail lengths
        if redStick:
            realBodyHeight = open - close
            tailHeight = close - low
            shadowLimit = realBodyHeight + open
        else: # open <= close:
            realBodyHeight = close - open
            tailHeight = open - low
            shadowLimit = realBodyHeight + close
        
        if tailHeight <= 2 * realBodyHeight:
            return False
        
        if high > shadowLimit:
                return False
        
        return True
    
    # The body may be red or green
    # Real Body deviation should be no more than 2%
    # Shadow must be at least 2*Body Height
    # Tail must be within 1 real body height of the open/close (whichever is lower)
    # Returns False if the specifications are not met, True if they are met.
    def is_inverted_hammer(self, stockData):
        try:
            high = analysis.getHigh(self, stockData, 1)
            low = analysis.getLow(self, stockData, 1)
            open = analysis.getOpen(self, stockData, 1)
            close = analysis.getClose(self, stockData, 1)
        except:
            return False 
            
        redStick = False
        
        # Check body deviation
        if open > close:
            redStick = True
            realBodyPercent = open/close - 1
        else: # open <= close:
            realBodyPercent = close/open - 1
            
        if realBodyPercent > .02:
            return False
        
        #Check shadow and tail lengths
        if redStick:
            realBodyHeight = open - close
            shadowHeight = high - open
            tailLimit = realBodyHeight + close
        else: # open <= close:
            realBodyHeight = close - open
            shadowHeight = high - close
            tailLimit = realBodyHeight + open
        
        if shadowHeight <= 2 * realBodyHeight:
            return False
        
        if low < tailLimit:
            return False
        
        return True
        
    # TODO analyze four+ previous days for red candlesticks; more likely to reverse
    # The Real Body of first day engulfs the high and low of the previous day
    # The previous 3 days (to include yesterday) must be Red Sticks
    def is_bullish_engulfing(self, stockData):
        try:
            openToday = analysis.getOpen(self, stockData, 1)
            closeToday = analysis.getClose(self, stockData, 1)
        
            highYesterday = analysis.getHigh(self, stockData, 2)
            lowYesterday = analysis.getLow(self, stockData, 2)
            open2 = analysis.getOpen(self, stockData, 2)
            close2 = analysis.getClose(self, stockData, 2)
            
            open3 = analysis.getOpen(self, stockData, 3)
            close3 = analysis.getClose(self, stockData, 3)
            
            open4 = analysis.getOpen(self, stockData, 4)
            close4 = analysis.getClose(self, stockData, 4)
        except:
            return False
            
        # If today is a Red Stick
        if openToday > closeToday:
            return False
        
        # If yesterday was not a Red Stick
        if open2 < close2:
            return False
        
        # If 2 days ago was not a Red Stick
        if open3 < close3:
            return False
        
        # If 3 days ago was not a Red Stick
        if open4 < close4:
            return False
        
        # If today's open does not cover yesterday's low
        if openToday > lowYesterday:
            return False
        
        # If today's close does not cover yesterdays high
        if closeToday < highYesterday:
            return False
        
        return True
    
    def checkPiercingLine(self, stockData):
        return
    
    def checkMorningStart(self, stockData):
        return
    
    def checkThreeWhiteSoldiers(self, stockData):
        return