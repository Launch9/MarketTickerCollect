from __future__ import print_function
from time import sleep
from bittrex_websocket import OrderBook
from datetime import datetime, timedelta
import time
import json
import os
import requests
def startNode(tickerz):
   
    while True:
        
        for i in tickerz:
            try:
                summary = get_history(i)
                curTime = time.time()
                summary['timestamp'] = curTime
                print("Writing to " + i)
                with open("./data/history/" + i + "/hist-" + str(curTime) + ".json", 'w') as json_file:
                    json.dump(summary, json_file)
                    json_file.close()
                sleep(2)
            except KeyboardInterrupt:
                exit()
            except:
                print("Caught exception!")
                sleep(5)
        
        print("Sleeping")
        sleep(60 * 60)

        
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

def get_history(trade):

    # api-endpoint
    url = "https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=" + trade
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
    if(os.path.isdir("./data/history") == False):
        print("Creating history folder.")
        os.mkdir("./data/history")
    else:
        print("Already created history folder.")
    for i in newMarketData:
        if(os.path.isdir("./data/history/" + i) == False):
            print("Creating " + i + " folder.")
            os.mkdir("./data/history/" + i)
        else:
            print("Already created " + i + " folder.")
    while(True):
        startNode(newMarketData)
        print("RESTARTING")


if __name__ == "__main__":
    main()