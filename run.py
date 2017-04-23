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


def get_balance():
    print(br.get_balances())
    # print(br.get_deposit_address('BTC'))
    # print(br.get_deposit_address('USDT'))
    print(bft.account_infos())


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
    get_balance()
    #bf_b, bf_s, br_b, br_s = get_ticker()
    #buy_sell(br_b, bf_s, br_b, br_s)
    #transfer()
    time.sleep(1)
