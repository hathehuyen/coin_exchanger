from __future__ import print_function
import config
# import polo
import btfx
import btrx
import json
import time


# p = polo.poloniex(config.POLO.APIKey, config.POLO.Secret)
# print(p.returnTicker())

bf = btfx.Client()
bft = btfx.TradeClient(config.BTFX.Key, config.BTFX.Secret)
br = btrx.Bittrex(config.BTRX.Key, config.BTRX.Secret)


def bitfinex_get_infos():
    def get_balance():
        btc_available = 0
        usd_available = 0
        balances = bft.get_balances()
        for balance in balances:
            if balance['type'] == 'exchange' and balance['currency'] == 'btc':
                btc_available = balance['available']
            if balance['type'] == 'exchange' and balance['currency'] == 'usd':
                usd_available = balance['available']
        # print('BTC: ', btc_available)
        # print('USD: ', usd_available)
        return float(usd_available), float(btc_available)

    def price_to_buy(order_book, amount):
        asks = order_book['asks']
        # print(asks)
        for ask in asks:
            if amount <= ask['amount']:
                return ask['price']
            else:
                amount -= float(ask['amount'])
        return False

    def price_to_sell(order_book, amount):
        bids = order_book['bids']
        # print(bids)
        for bid in bids:
            if amount <= bid['amount']:
                return bid['price']
            else:
                amount -= float(bid['amount'])
        return False

    order_book = bf.order_book('BTCUSD')
    usd_available, btc_available = get_balance()
    # print(price_to_buy(order_book, 6))
    # print(price_to_sell(order_book, 6))
    return usd_available, btc_available,\
           price_to_buy(order_book, usd_available), price_to_sell(order_book, btc_available)


def run():
    # print(br.get_balances())
    # print(br.get_deposit_address('BTC'))
    # print(br.get_deposit_address('USDT'))
    pass
    # print(bft.account_infos())
    # print(bft.get_summary())
    # print(bft.get_deposit_address('bitcoin'))
    # print(bft.get_deposit_address('mastercoin'))
    # print(json.dumps(bf.order_book('BTCUSD')))


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
    usd_available, btc_available, price_to_buy, price_to_sell = bitfinex_get_infos()
    print(usd_available, btc_available, price_to_buy, price_to_sell)
    print('Buy all BTC: ', usd_available / price_to_buy + btc_available)
    print('Sell all BTC: ', btc_available * price_to_sell + usd_available)
    # run()
    #calculate_price_and_amount()
    # bf_b, bf_s, br_b, br_s = get_ticker()
    # buy_sell(br_b, bf_s, br_b, br_s)
    # transfer()
    time.sleep(1)
