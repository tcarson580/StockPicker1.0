'''
Created on Sep 3, 2019

@author: FN-1776
'''
from numpy.core.defchararray import lower

def test_stock(high, low, open, close):
    stockData = {
        "high": high,
        "low": low,
        "open": open,
        "close": close
        }
    return stockData
