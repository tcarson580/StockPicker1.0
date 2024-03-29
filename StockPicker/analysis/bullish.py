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
    @staticmethod
    def is_hammer(stockData):
        try:
            high = analysis.getHigh(stockData, 1)
            low = analysis.getLow(stockData, 1)
            open = analysis.getOpen(stockData, 1)
            close = analysis.getClose(stockData, 1)
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
    @staticmethod
    def is_inverted_hammer(stockData):
        try:
            high = analysis.getHigh(stockData, 1)
            low = analysis.getLow(stockData, 1)
            open = analysis.getOpen(stockData, 1)
            close = analysis.getClose(stockData, 1)
        except:
            return False 
            
        redStick = False
        
        # Check body deviation for more than 2%
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
    @staticmethod
    def is_bullish_engulfing(stockData):
        try:
            openToday = analysis.getOpen(stockData, 1)
            closeToday = analysis.getClose(stockData, 1)
        
            highYesterday = analysis.getHigh(stockData, 2)
            lowYesterday = analysis.getLow(stockData, 2)
            open2 = analysis.getOpen(stockData, 2)
            close2 = analysis.getClose(stockData, 2)
            
            open3 = analysis.getOpen(stockData, 3)
            close3 = analysis.getClose(stockData, 3)
            
            open4 = analysis.getOpen(stockData, 4)
            close4 = analysis.getClose(stockData, 4)
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
    
    # Yesterday is Red Stick
    # Today is Green Stick
    # Today's open is less than yesterday's low
    # Today's close is more than halfway up yesterday's Real Body
    @staticmethod
    def is_piercing_line(stockData):
        try:
            openToday = analysis.getOpen(stockData, 1)
            closeToday = analysis.getClose(stockData, 1)
            highToday = analysis.getHigh(stockData, 1)
            lowToday = analysis.getLow(stockData, 1)
            
            openYesterday = analysis.getOpen(stockData, 2)
            closeYesterday = analysis.getClose(stockData, 2)
            highYesterday = analysis.getHigh(stockData, 2)
            lowYesterday = analysis.getLow(stockData, 2)
        except:
            return False
        
        # If yesterday is not a Red Stick
        if openYesterday < closeYesterday:
            return False
        
        # If today is a Red Stick
        if openToday > closeToday:
            return False
        
        # If today's open is greater than yesterday's low
        if openToday >= lowYesterday:
            return False
        
        halfRealBodyYesterday = (openYesterday + closeYesterday)/2
        
        # If today's close is less than halfway up yesterday's Real Body
        if closeToday < halfRealBodyYesterday:
            return False
        
        return True
    
    @staticmethod
    def is_morning_star(stockData):
        try:
            openToday = analysis.getOpen(stockData, 1)
            closeToday = analysis.getClose(stockData, 1)
            highToday = analysis.getHigh(stockData, 1)
            lowToday = analysis.getLow(stockData, 1)
            
            openYesterday = analysis.getOpen(stockData, 2)
            closeYesterday = analysis.getClose(stockData, 2)
            highYesterday = analysis.getHigh(stockData, 2)
            lowYesterday = analysis.getLow(stockData, 2)
            
            open3 = analysis.getOpen(stockData, 3)
            close3 = analysis.getClose(stockData, 3)
            high3 = analysis.getHigh(stockData, 3)
            low3 = analysis.getLow(stockData, 3)
        except:
            return False
        
        # If today is a Red Stick
        if openToday > closeToday:
            return False
        
        # If yesterday was a Red Stick
        if openYesterday > closeYesterday:
            return False
        
        # If 2 days ago was not a Red Stick
        if close3 > open3:
            return False
        
        # Check body deviations
        realBodyPercentToday = closeToday/openToday - 1
        realBodyPercentYesterday = closeYesterday/openYesterday - 1
        realBodyPercent3 = open3/close3 - 1
        
        # If today has a body deviation smaller than 4%    
        if realBodyPercentToday < .04:
            return False
        
        # If yesterday has a body deviation greater than 2%
        if realBodyPercentYesterday > .02:
            return False
        
        # If 2 days ago has a body deviation smaller than 4%  
        if realBodyPercent3 < .04:
            return False
        
        # If yesterday's body does not occur below 2 days ago's close
        if closeYesterday > close3:
            return False
        
        # If yesterday's body does not occur below today's open
        if closeYesterday > openToday:
            return False
        
        return True
    
    # 3 consecutive Green Sticks
    # Body Deviation for each 3 must be at least 3%
    # Each day's open must be greater than the previous days'
    # Each day's close must be greater than the previous days'
    @staticmethod
    def is_three_white_soldiers(stockData):
        try:
            openToday = analysis.getOpen(stockData, 1)
            closeToday = analysis.getClose(stockData, 1)
            highToday = analysis.getHigh(stockData, 1)
            #lowToday = analysis.getLow(stockData, 1)
            
            openYesterday = analysis.getOpen(stockData, 2)
            closeYesterday = analysis.getClose(stockData, 2)
            highYesterday = analysis.getHigh(stockData, 2)
            #lowYesterday = analysis.getLow(stockData, 2)
            
            open3 = analysis.getOpen(stockData, 3)
            close3 = analysis.getClose(stockData, 3)
            high3 = analysis.getHigh(stockData, 3)
            
            #low3 = analysis.getLow(stockData, 3)
        except:
            return False
        
        # If today is a Red Stick
        if openToday > closeToday:
            return False
        
        # If yesterday was a Red Stick
        if openYesterday > closeYesterday:
            return False
        
        # If 2 days ago was a Red Stick
        if open3 > close3:
            return False
        
        # Check body deviations
        realBodyPercentToday = closeToday/openToday - 1
        realBodyPercentYesterday = closeYesterday/openYesterday - 1
        realBodyPercent3 = close3/open3 - 1
        
        # If today's a body deviation smaller than 3%  
        if realBodyPercentToday < .03:
            return False
        
        # If yesterday's body deviation smaller than 3%  
        if realBodyPercentYesterday < .03:
            return False
        
        # If 2 days ago has a body deviation smaller than 3%  
        if realBodyPercent3 < .03:
            return False
        
        realBodyHeightToday = closeToday - openToday
        realBodyHeightYesterday = closeYesterday - openYesterday
        realBodyHeight3 = close3 - open3
        
        shadowLimitToday = realBodyHeightToday + closeToday
        shadowLimitYesterday = realBodyHeightYesterday + closeYesterday
        shadowLimit3 = realBodyHeight3 + close3
        
        # If today's high is greater than one Real Body Height
        if highToday > shadowLimitToday:
            return False
        
        # If yesterday's high is greater than one Real Body Height
        if highYesterday > shadowLimitYesterday:
            return False
        
        # If 2 days ago's high is greater than one Real Body Height
        if high3 > shadowLimit3:
            return False
        
        # If the open today is not greater than the open yesterday
        if openToday < openYesterday:
            return False
        
        # If the open yesterday is not greater than the open 2 days ago
        if openYesterday < open3:
            return False
        
        # If the close today is not greater than the close yesterday
        if closeToday < closeYesterday:
            return False
        
        # If the close yesterday is not greater than the close 2 days ago
        if closeYesterday < close3:
            return False
        
        return True