from __future__ import print_function
import config
# import polo
import btfx
import btrx
import json
import time
import db


# p = polo.poloniex(config.POLO.APIKey, config.POLO.Secret)
# print(p.returnTicker())

bf = btfx.Client()
bft = btfx.TradeClient(config.BTFX.Key, config.BTFX.Secret)
br = btrx.Bittrex(config.BTRX.Key, config.BTRX.Secret)


def run():
    # print(br.get_balances())
    # print(br.get_deposit_address('BTC'))
    # print(br.get_deposit_address('USDT'))
    btc_available = 0
    usd_available = 0
    balances = bft.get_balances()
    for balance in balances:
        if balance['type'] == 'exchange' and balance['currency'] == 'btc':
            btc_available = balance['available']
        if balance['type'] == 'exchange' and balance['currency'] == 'usd':
            usd_available = balance['available']
    print('BTC: ', btc_available)
    print('USD: ', usd_available)

    
    # print(bft.account_infos())
    # print(bft.get_summary())
    # print(bft.get_deposit_address('bitcoin'))
    # print(bft.get_deposit_address('mastercoin'))
    # print(json.dumps(bf.order_book('BTCUSD')))

def calculate_price_and_amount(symbol='BTCUSD'):
    result = bf.order_book(symbol)
    bids = result['bids']
    bid_want_price = 1370
    bid_amount = 0
    asks = result['asks']
    ask_want_price = 1380
    ask_amount = 0
    for bid in bids:
        if bid['price'] >= bid_want_price:
            bid_amount += bid['amount']
        #print(bid)
    print(bid_amount)
    for ask in asks:
        if ask['price'] <= ask_want_price:
            ask_amount += ask['price']
    print(ask_amount)
        #print(ask)


def get_ticker():
    bf_ticker = json.loads(bf.ticker('btcusd'))
    br_ticker = json.loads(br.get_ticker('USDT-BTC'))
    bf_btc_buy_price = bf_ticker.ask
    bf_btc_sell_price = bf_ticker.bid
    br_btc_buy_price = br_ticker.result.Ask
    br_btc_sell_price = br_ticker.result.Bid
    return bf_btc_buy_price, bf_btc_sell_price, br_btc_buy_price, br_btc_sell_price


def buy_sell(bf_btc_buy_price, bf_btc_sell_price, br_btc_buy_price, br_btc_sell_price):
    def buy_br():
        pass

    def sell_bf():
        pass

    def buy_bf():
        pass

    def sell_br():
        pass

    if bf_btc_buy_price < br_btc_sell_price:
        sell_br()
        buy_bf()
    if br_btc_buy_price < bf_btc_sell_price:
        buy_br()
        sell_bf()


def transfer():
    pass


if __name__ == "__main__":
    run()
    #calculate_price_and_amount()
    # bf_b, bf_s, br_b, br_s = get_ticker()
    # buy_sell(br_b, bf_s, br_b, br_s)
    # transfer()
    time.sleep(1)