from __future__ import print_function
from time import sleep
from bittrex_websocket import OrderBook
from datetime import datetime, timedelta
import time
import json
import os
import requests
def startNode(tickerz):
    class MySocket(OrderBook):
        def on_ping(self, msg):
            print("Pinged!")
            
            
            
                    

    # Create the socket instance
    ws = MySocket()
    # Enable logging
    ws.enable_log()
    # Define tickers
    tickers = tickerz
    # Subscribe to order book updates
    latest_ping = datetime.now()
    totalTime = 60 #In seconds
    sleepTime = totalTime / len(tickers)
    print("Sleep time is: " + str(sleepTime))
    
    while True:
        try:
            ws.query_exchange_state(tickers[0:int(len(tickers)/2)])
            for i in tickers[0:int(len(tickers)/2)]:
                book = ws.get_order_book(i)
                if(book != None):
                    book['timestamp'] = time.time()
                    print("Writing to file!1: " + i)
                    latest_ping = datetime.now()
                    sleep(sleepTime)
                    with open("./data/" + book['ticker'] + "/" + book['ticker'] + ":" + str(book['timestamp']) + ".json", 'w') as json_file:
                        json.dump({"book":book}, json_file)
                        json_file.close()
            ws.query_exchange_state(tickers[int(len(tickers)/2):len(tickers)])
            for i in tickers[int(len(tickers)/2):len(tickers)]:
                book = ws.get_order_book(i)
                if(book != None):
                    book['timestamp'] = time.time()
                    print("Writing to file!2: " + i)
                    latest_ping = datetime.now()
                    sleep(sleepTime)
                    with open("./data/" + book['ticker'] + "/" + book['ticker'] + ":" + str(book['timestamp']) + ".json", 'w') as json_file:
                        json.dump({"book":book}, json_file)
                        json_file.close()



            delta = (datetime.now() - latest_ping)
            print("Latest delta: " + str(float(delta.seconds)))
        except:
            print("Threw exception!")
            return False
        
        try:
            summary = get_markets()
            curTime = time.time()
            summary['timestamp'] = curTime
            with open("./data/summaries/summary-" + str(curTime) + ".json", 'w') as json_file:
                json.dump(summary, json_file)
                json_file.close()
        except:
            print("Caught exception!")
        
        try:
            if(delta != None):
                if(delta.seconds > 480):
                    return False
                if(delta.seconds < totalTime - (sleepTime * (len(tickers) / 2))):
                    print("No new updates. Sleeping for 30 seconds")
                    sleep(30)
        except:
            print("Threw exception!")
    else:
        pass

def get_markets():

    # api-endpoint
    url = "https://bittrex.com/api/v2.0/pub/markets/GetMarketSummaries"
    #"https://api.bittrex.com/api/v1.1/public/getmarketsummaries"
    #url = "https://api.bittrex.com/v3/markets/" + trade_string + "/candles?candleInterval=" + interval
    headers = {
        'Accepts': 'application/json',
    }
    # sending get request and saving the response as response object
    r = requests.get(url=url, headers=headers, verify=True)
    if (r.ok == False):
        return False
    else:
        return r.json()

def main():
    newMarketData = []
    # api-endpoint
    marketData = get_markets()['result']
    for i in marketData:
        newMarketData.append(i["Summary"]["MarketName"])
    for i in newMarketData:
        if(os.path.isdir("./data/" + i) == False):
            print("Creating " + i + " folder.")
            os.mkdir("./data/" + i)
        else:
            print("Already created " + i + " folder.")
    if(os.path.isdir("./data/summaries") == False):
        print("Creating summaries folder.")
        os.mkdir("./data/summaries")
    else:
        print("Already created summaries folder.")
    while(True):
        startNode(newMarketData)
        print("RESTARTING")


if __name__ == "__main__":
    main()