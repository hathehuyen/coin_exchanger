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
        if 'success' in balances:
            if balances['success']:
                for balance in balances['result']:
                    if balance['Currency'] == 'BTC':
                        btc_available = balance['Available']
                    if balance['Currency'] == 'USDT':
                        usd_available = balance['Available']
                # print_info('BTC: ', btc_available)
                # print_info('USD: ', usd_available)
                return float(usd_available), float(btc_available)

    def price_to_buy(order_book, amount):
        if 'success' in order_book:
            if order_book['success']:
                asks = order_book['result']['sell']
                # print_info(asks)
                for ask in asks:
                    if amount <= ask['Quantity'] * ask['Rate']:
                        return ask['Rate']
                    else:
                        amount -= float(ask['Quantity'] * ask['Rate'])
        return False

    def price_to_sell(order_book, amount):
        if 'success' in order_book:
            if order_book['success']:
                bids = order_book['result']['buy']
                # print_info(asks)
                for bid in bids:
                    if amount <= bid['Quantity']:
                        return bid['Rate']
                    else:
                        amount -= float(bid['Quantity'])
        return False

    # usd_available, btc_available = get_balance()
    # order_book = br.get_orderbook('USDT-BTC', 'both')
    order_book = pl.returnOrderBook('usdt-btc')
    print ("Order book")
    print (order_book)
    # return usd_available, btc_available, \
    #        price_to_buy(order_book, usd_available), price_to_sell(order_book, btc_available)

if __name__ == '__main__':
    print ("RUN")
    polo_get_infos()
