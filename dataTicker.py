from __future__ import print_function
from time import sleep
from bittrex_websocket import OrderBook
from datetime import datetime, timedelta
import json
import os
def startNode(tickerz):
    class MySocket(OrderBook):
        latest_ping = datetime.now()
        def on_ping(self, msg):
            self.latest_ping = datetime.now()
            
            
            
            
                    

    # Create the socket instance
    ws = MySocket()
    # Enable logging
    ws.enable_log()
    # Define tickers
    tickers = tickerz
    # Subscribe to order book updates
    ws.subscribe_to_orderbook(tickers)
    
    while True:
        for i in tickers:
            book = ws.get_order_book(i)
            if(book != None):
                if('timestamp' in book):
                    with open("./data/" + book['ticker'] + "/" + book['ticker'] + ":" + str(book['timestamp']) + ".json", 'w') as json_file:
                        #json.dump({"book": book, "data": getOrderData(book)}, json_file)
                        json.dump({"book":book}, json_file)
                        json_file.close()
                    
        
        delta = (datetime.now() - ws.latest_ping)
        print("Latest delta: " + str(float(delta.seconds)))
        
        if(delta != None):
            if(delta.seconds > 120):
                return False
            
                
        
        sleep(30)
    else:
        pass

def main():
    
    marketData = ['BTC-LTC','BTC-BAT','BTC-TUSD', 'BTC-XRP', 'USDT-XMR', 'USDT-BTC', 'ETH-XRP', 'ETH-NEO', 'ETH-XMR', 'BTC-XMR', 'BTC-GAME', 'BTC-BSV', 'BTC-DGB']#get_market_summaries()
    for i in marketData:
        
        if(os.path.isdir("./data/" + i) == False):
            print("Creating " + i + " folder.")
            os.mkdir("./data/" + i)
        else:
            print("Already created " + i + " folder.")
    while(True):
        startNode(marketData)
        print("RESTARTING")


if __name__ == "__main__":
    main()