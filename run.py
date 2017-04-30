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
            if amount <= ask['amount'] * ask['price']:
                return ask['price']
            else:
                amount -= float(ask['amount'] * ask['price'])
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

    def get_fee():
        print(bft.account_infos())

    order_book = bf.order_book('BTCUSD')
    usd_available, btc_available = get_balance()
    # print(price_to_buy(order_book, 6))
    # print(price_to_sell(order_book, 6))
    return usd_available, btc_available,\
           price_to_buy(order_book, usd_available), price_to_sell(order_book, btc_available)


def bittrex_get_infos():
    def get_balance():
        btc_available = 0
        usd_available = 0
        balances = br.get_balances()
        # print(balances)
        if 'success' in balances:
            if balances['success']:
                for balance in balances['result']:
                    if balance['Currency'] == 'BTC':
                        btc_available = balance['Available']
                    if balance['Currency'] == 'USDT':
                        usd_available = balance['Available']
                # print('BTC: ', btc_available)
                # print('USD: ', usd_available)
                return float(usd_available), float(btc_available)

    def price_to_buy(order_book, amount):
        if 'success' in order_book:
            if order_book['success']:
                asks = order_book['result']['sell']
                # print(asks)
                for ask in asks:
                    if amount <= ask['Quantity'] * ask['Rate'] :
                        return ask['Rate']
                    else:
                        amount -= float(ask['Quantity'] * ask['Rate'])
        return False

    def price_to_sell(order_book, amount):
        if 'success' in order_book:
            if order_book['success']:
                bids = order_book['result']['buy']
                # print(asks)
                for bid in bids:
                    if amount <= bid['Quantity']:
                        return bid['Rate']
                    else:
                        amount -= float(bid['Quantity'])
        return False

    usd_available, btc_available = get_balance()
    order_book = br.get_orderbook('USDT-BTC', 'both')
    return usd_available, btc_available, \
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
    try:
        #print(json.dumps(bft.get_summary()))
        while True:
            try:
                # Bitfinex
                bf_usd_available, bf_btc_available, bf_price_to_buy, bf_price_to_sell = bitfinex_get_infos()
                print(bf_usd_available, bf_btc_available, bf_price_to_buy, bf_price_to_sell)
                print(bf.ticker('btcusd'))
                # print('Buy all BTC: ',
                #       (usd_available / price_to_buy) - (usd_available / price_to_buy) * config.BTFX.taker_fee  + btc_available)
                # print('Sell all BTC: ',
                #       btc_available * price_to_sell - (btc_available * price_to_sell) * config.BTFX.taker_fee+ usd_available)
                # print(bft.place_order(str((usd_available / price_to_buy) - (usd_available / price_to_buy) * config.BTFX.taker_fee),
                #       str(price_to_buy), "buy", "exchange fill-or-kill"))
                # print(json.dumps({u'oco_order': None, u'was_forced': False, u'src': u'api', u'avg_execution_price': u'0.0', u'exchange': u'bitfinex', u'order_id': 2402375671, u'timestamp': u'1493396216.368241535', u'symbol': u'btcusd', u'cid': 58616340437, u'cid_date': u'2017-04-28', u'price': u'1398.1', u'is_live': True, u'gid': None, u'executed_amount': u'0.0', u'is_cancelled': False, u'remaining_amount': u'0.0214596921373', u'is_hidden': False, u'original_amount': u'0.0214596921373', u'type': u'exchange fok', u'id': 2402375671, u'side': u'buy'}))
                # print(json.dumps(bft.status_order(2402375671)))

                # Bitfinex
                br_usd_available, br_btc_available, br_price_to_buy, br_price_to_sell = bittrex_get_infos()
                print(br_usd_available, br_btc_available, br_price_to_buy, br_price_to_sell)
                print(br.get_ticker('USDT-BTC'))

                # Compare to make decision
                fee = 0
                price_delta_br_bf = bf_price_to_sell - br_price_to_buy
                price_delta_bf_br = br_price_to_sell - bf_price_to_buy
                if price_delta_br_bf > fee:
                    print ('br->bf: ',  price_delta_br_bf)

                if price_delta_bf_br > fee:
                    print ('bf->br: ', price_delta_bf_br)
                # print('Buy all BTC: ',
                #       (usd_available / price_to_buy) - (usd_available / price_to_buy) * config.BTFX.taker_fee  + btc_available)
                # print('Sell all BTC: ',
                #       btc_available * price_to_sell - (btc_available * price_to_sell) * config.BTFX.taker_fee+ usd_available)
                # run()
                #calculate_price_and_amount()
                # bf_b, bf_s, br_b, br_s = get_ticker()
                # buy_sell(br_b, bf_s, br_b, br_s)
                # transfer()
            except Exception as ex:
                print(ex.message)
            time.sleep(15)
    except Exception as ex:
        raise ex
