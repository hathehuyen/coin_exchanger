from __future__ import print_function
import config
import polo
import btfx
import btrx
import json
import time
import logging
from datetime import datetime


logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',level=logging.DEBUG)
#
# bf = btfx.Client()
# bft = btfx.TradeClient(config.BTFX.Key, config.BTFX.Secret)
# br = btrx.Bittrex(config.BTRX.Key, config.BTRX.Secret)
pl = polo.poloniex(config.POLO.Key, config.POLO.Secret)

def polo_get_infos():
    def get_balance():
        btc_available = 0
        usd_available = 0
        balances = pl.returnBalances()

        print(balances)
        usd_available = balances['USDT']
        btc_available = balances['BTC']
        # print (usd_available, " ", btc_available)
        return float(usd_available), float(btc_available)

    def price_to_buy(order_book, amount):
        asks = order_book['asks']
        # print_info(asks)
        for ask in asks:
            if amount <= ask[1] * float(ask[0]):
                return float(ask[0])
            else:
                amount -= float(ask[1] * float(ask[0]))
        return False

    def price_to_sell(order_book, amount):
        bids = order_book['bids']
        for bid in bids:
            if amount <= bid[1]:
                return float(bid[0])
            else:
                amount -= float(bid[1])
        return False
    usd_available, btc_available = get_balance()
    order_book = pl.returnOrderBook('USDT_BTC')
    print(order_book['bids'][0][0])
    print(order_book['bids'][0])
    print ("Order book")
    print (order_book)

    print(usd_available, btc_available,
                price_to_buy(order_book, usd_available), price_to_sell(order_book, btc_available))
    # return usd_available, btc_available, \
    #        price_to_buy(order_book, usd_available), price_to_sell(order_book, btc_available)

if __name__ == '__main__':
    print ("RUN")
    polo_get_infos()
