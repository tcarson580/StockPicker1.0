'''
Created on Aug 31, 2019

@author: FN-1776
'''

import retrieve.retriever as retriever

if __name__ == '__main__':
    client = retriever.StockDataRetriever()
    print(client.getData("TSLA", '2015-08-19', '2019-08-023')[0])

