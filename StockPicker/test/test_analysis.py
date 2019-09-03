'''
Created on Sep 3, 2019

@author: FN-1776
'''
import unittest
import test.test_stock as stock
from analysis.bullish import BullishAnalysis as bullish

# Test stocks must be placed into list due to possibility for 
# multiple stocks being required to meet candlestick definitions
class TestAnalysis(unittest.TestCase):
    def test_checkHammer(self):
        # Red stock, Real body < 2%, Shadow > 2* Real body
        testStock = [stock.test_stock(100, 10, 80, 79)]
        self.assertEquals(bullish.check_hammer(self, testStock), True)
        
        # Green stock, Real body < 2%, Shadow > 2* Real body
        testStock = [stock.test_stock(100, 10, 79, 80)]
        self.assertEquals(bullish.check_hammer(self, testStock), True)
        
        # Red stock, Real body < 2%, Shadow = 2* Real body
        testStock = [stock.test_stock(100, 77, 80, 79)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Green stock, Real body < 2%, Shadow = 2* Real body
        testStock = [stock.test_stock(100, 77, 79, 80)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Red stock, Real body < 2%, Shadow < 2* Real body
        testStock = [stock.test_stock(100, 78, 80, 79)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Green stock, Real body < 2%, Shadow < 2* Real body
        testStock = [stock.test_stock(100, 78, 79, 80)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Red stock, Real body = 2%, Shadow > 2* Real body
        testStock = [stock.test_stock(100, 10, 80, 78.4)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Green stock, Real body = 2%, Shadow > 2* Real body
        testStock = [stock.test_stock(100, 10, 78.4, 80)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Red stock, Real body = 2%, Shadow = 2* Real body
        testStock = [stock.test_stock(100, 74.8, 80, 78.4)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Green stock, Real body = 2%, Shadow = 2* Real body
        testStock = [stock.test_stock(100, 74.8, 78.4, 80)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Red stock, Real body = 2%, Shadow < 2* Real body
        testStock = [stock.test_stock(100, 73, 80, 78.4)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Green stock, Real body = 2%, Shadow < 2* Real body
        testStock = [stock.test_stock(100, 73, 78.4, 80)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Red stock, Real body > 2%, Shadow > 2* Real body
        testStock = [stock.test_stock(100, 10, 80, 78)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Green stock, Real body > 2%, Shadow > 2* Real body
        testStock = [stock.test_stock(100, 10, 78, 80)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Red stock, Real body > 2%, Shadow = 2* Real body
        testStock = [stock.test_stock(100, 74.8, 80, 78)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Green stock, Real body > 2%, Shadow = 2* Real body
        testStock = [stock.test_stock(100, 74.8, 78, 80)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Red stock, Real body > 2%, Shadow < 2* Real body
        testStock = [stock.test_stock(100, 73, 80, 78)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)
        
        # Green stock, Real body > 2%, Shadow < 2* Real body
        testStock = [stock.test_stock(100, 73, 78, 80)]
        self.assertEquals(bullish.check_hammer(self, testStock), False)

    def test_checkInverseHammer(self):
        self.assertEquals(True, True)
    
    def test_checkBullishEngulfing(self):
        self.assertEquals(True, True)
    
    def test_checkPiercingLine(self):
        self.assertEquals(True, True)
    
    def test_checkMorningStart(self):
        self.assertEquals(True, True)
    
    def test_checkThreeWhiteSoldiers(self):
        self.assertEquals(True, True)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()