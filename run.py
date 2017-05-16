from __future__ import print_function
import config
# import polo
import btfx
import btrx
import json
import time


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
    return usd_available, btc_available, \
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
                    if amount <= ask['Quantity'] * ask['Rate']:
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


def bitfinex_buy(usd_amount, price_to_buy):
    try:
        order = bft.place_order(str(usd_amount / price_to_buy), str(price_to_buy), "buy", "exchange fill-or-kill")
        print(order)
        if 'order_id' in order:
            order_id = order['order_id']
            order_status = bft.status_order(order_id)
            print(order_status)
            if order_status['executed_amount'] == order_status['original_amount']:
                return True
        return False
    except Exception as ex:
        print(ex)
        return False


def bitfinex_sell(amount, price_to_sell):
    try:
        order = bft.place_order(str(amount), str(price_to_sell), "sell", "exchange fill-or-kill")
        print(order)
        if 'order_id' in order:
            order_id = order['order_id']
            order_status = bft.status_order(order_id)
            print(order_status)
            if order_status['executed_amount'] == order_status['original_amount']:
                return True
        return False
    except Exception as ex:
        print(ex)
        return False


def bittrex_buy(usd_amount, price_to_buy):
    market = 'USDT-BTC'
    try:
        # Buy BTC
        order = br.buy_limit(market, usd_amount / price_to_buy, price_to_buy)
        if order.get('success'):
            order_result = order.get('result')
            uuid = order_result.get('uuid')
            # Check open order
            if uuid:
                open_orders = br.get_open_orders(market)
                if open_orders.get('success'):
                    open_orders_result = open_orders.get('result')
                    if open_orders_result:
                        for open_order in open_orders_result:
                            if uuid == open_order.get('OrderUuid'):
                                # Cancel
                                br.cancel(uuid)
                                return False
        return True
    except Exception as ex:
        print(ex)
        return False


def bittrex_sell(btc_amount, price_to_sell):
    market = 'USDT-BTC'
    try:
        # Sell BTC
        order = br.sell_limit(market, btc_amount, price_to_sell)
        if order.get('success'):
            order_result = order.get('result')
            uuid = order_result.get('uuid')
            # Check open order
            if uuid:
                open_orders = br.get_open_orders(market)
                if open_orders.get('success'):
                    open_orders_result = open_orders.get('result')
                    if open_orders_result:
                        for open_order in open_orders_result:
                            if uuid == open_order.get('OrderUuid'):
                                # Cancel
                                br.cancel(uuid)
                                return False
        return True
    except Exception as ex:
        print(ex)
        return False


# print(br.get_balances())
# print(br.get_deposit_address('BTC'))
# print(br.get_deposit_address('USDT'))
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


def transfer():
    pass


if __name__ == "__main__":
    try:
        # print(json.dumps(bft.get_summary()))
        # print(json.dumps(bft.active_offers()))
        while True:
            try:
                print('=== running ===')
                # Get Bitfinex info
                bf_usd_available, bf_btc_available, bf_price_to_buy, bf_price_to_sell = bitfinex_get_infos()
                print('Bitfinex: ', bf_usd_available, bf_btc_available, bf_price_to_buy, bf_price_to_sell)
                # Get Bittrex info
                br_usd_available, br_btc_available, br_price_to_buy, br_price_to_sell = bittrex_get_infos()
                print('Bittrex: ', br_usd_available, br_btc_available, br_price_to_buy, br_price_to_sell)
                #test data
                br_usd_available = 1000
                bf_usd_available = 1000
                br_btc_available = 0.5
                bf_btc_available = 0.5
                # Compare to make decision
                price_delta_br_bf = bf_price_to_sell - br_price_to_buy
                price_delta_bf_br = br_price_to_sell - bf_price_to_buy
                print('Total usd available: ', bf_usd_available + br_usd_available)
                print('Total btc available: ', br_btc_available + bf_btc_available)
                total_before_exchange = br_usd_available + bf_usd_available + \
                                        br_btc_available * br_price_to_sell + bf_btc_available * bf_price_to_sell
                print('Total value before exchange: ', total_before_exchange)
                if price_delta_br_bf > 0:
                    print('br->bf: ', price_delta_br_bf)
                    btc_after_buy = (br_usd_available - br_usd_available * config.BTRX.taker_fee) / br_price_to_buy \
                                    + br_btc_available
                    usd_after_sell = (bf_btc_available - bf_btc_available * config.BTFX.taker_fee) * bf_price_to_sell \
                                     + br_usd_available
                    usd_after_transfer = usd_after_sell - config.BTFX.withdraw_fee['USDT']
                    btc_after_transfer = btc_after_buy - config.BTRX.withdraw_fee['BTC']
                    print('btc after transfer ', btc_after_transfer)
                    print('usd after transfer ', usd_after_transfer)
                    total_after_transfer = usd_after_transfer + btc_after_transfer * br_price_to_sell / 2 \
                                            + btc_after_transfer * bf_price_to_sell / 2
                    print('Total value after exchange: ', total_after_transfer)
                    earned = total_after_transfer - total_before_exchange
                    earned_percent = earned / total_before_exchange * 100
                    print('Earned: ', earned, ' (', earned_percent, ' percent)')
                    if earned_percent >= config.min_rate_per_exchange:
                        if bittrex_buy(br_usd_available, br_price_to_buy):
                            if bitfinex_sell(bf_btc_available, bf_price_to_sell):
                                print('Buy and sell complete, transfering coin')
                                bft.withdraw('mastercoin', str(usd_after_sell / 2),config.BTRX.wallet_adress['USDT'])
                                br.withdraw('BTC', btc_after_buy / 2, config.BTFX.wallet_adress['BTC'])
                                print('Transfer oder placed, waiting for received')
                                received = False
                                while not received:
                                    time.sleep(config.time_to_sleep)
                                    print('Checking if coins received')
                                    bf_usd_available, bf_btc_available, bf_price_to_buy, bf_price_to_sell \
                                        = bitfinex_get_infos()
                                    br_usd_available, br_btc_available, br_price_to_buy, br_price_to_sell \
                                        = bittrex_get_infos()
                                    if abs(br_usd_available - br_usd_available) < 1 and \
                                                    abs(br_btc_available - bf_btc_available) < 0.001:
                                        received = True
                                        print('Coins received')
                            else:
                                print('Buy complete, sell failed')
                                sell_complete = False
                                last_buy_price = br_price_to_buy
                                while not sell_complete:
                                    time.sleep(config.time_to_sleep)
                                    bf_usd_available, bf_btc_available, bf_price_to_buy, bf_price_to_sell \
                                        = bitfinex_get_infos()
                                    br_usd_available, br_btc_available, br_price_to_buy, br_price_to_sell \
                                        = bittrex_get_infos()
                                    usd_after_sell = (bf_btc_available - bf_btc_available * config.BTFX.taker_fee) \
                                                     * bf_price_to_sell + br_usd_available
                                    usd_after_transfer = usd_after_sell - config.BTFX.withdraw_fee['USDT']
                                    if bf_price_to_sell > last_buy_price:
                                        if bitfinex_sell(bf_btc_available, bf_price_to_sell):
                                            sell_complete = True
                                            print('Sell complete on Bitfinex, transfering coin')
                                            bft.withdraw('mastercoin', str(usd_after_sell / 2),
                                                         config.BTRX.wallet_adress['USDT'])
                                            br.withdraw('BTC', btc_after_buy / 2, config.BTFX.wallet_adress['BTC'])
                                            print('Transfer oder placed, waiting for received')
                                            received = False
                                            while not received:
                                                time.sleep(config.time_to_sleep)
                                                print('Checking if coins received')
                                                bf_usd_available, bf_btc_available, bf_price_to_buy, bf_price_to_sell \
                                                    = bitfinex_get_infos()
                                                br_usd_available, br_btc_available, br_price_to_buy, br_price_to_sell \
                                                    = bittrex_get_infos()
                                                if abs(br_usd_available - br_usd_available) < 1 and \
                                                                abs(br_btc_available - bf_btc_available) < 0.001:
                                                    received = True
                                                    print('Coins received')
                                    if br_price_to_sell > last_buy_price:
                                        if bittrex_sell(br_btc_available / 2, br_price_to_sell):
                                            sell_complete = True
                                            print('Resell complete on Bittrex')
                if price_delta_bf_br > 0:
                    print('bf->br: ', price_delta_bf_br)
                    btc_after_buy = (bf_usd_available - bf_usd_available * config.BTFX.taker_fee) / bf_price_to_buy \
                                    + bf_btc_available
                    usd_after_sell = (br_btc_available - br_btc_available * config.BTRX.taker_fee) * br_price_to_sell \
                                     + br_usd_available
                    usd_after_transfer = usd_after_sell - config.BTRX.withdraw_fee['USDT']
                    btc_after_transfer = btc_after_buy - config.BTFX.withdraw_fee['BTC']
                    print('btc after transfer ', btc_after_transfer)
                    print('usd after transfer ', usd_after_transfer)
                    total_after_transfer = usd_after_transfer + btc_after_transfer * br_price_to_sell / 2 \
                                           + btc_after_transfer * bf_price_to_sell / 2
                    print('Total value after exchange: ', total_after_transfer)
                    earned = total_after_transfer - total_before_exchange
                    earned_percent = earned / total_before_exchange * 100
                    print('Earned: ', earned, ' (', earned_percent, ' percent)')
                    if earned_percent >= config.min_rate_per_exchange:
                        pass
                # # Test buy all bitfinex
                # if bitfinex_buy(bf_usd_available, bf_price_to_buy):
                #     print("Buy complete")
                # else:
                #     print("Buy failed")
                # # Test sell all bitfinex
                # if bitfinex_sell(bf_btc_available, bf_price_to_sell):
                #     print("Sell complete")
                # else:
                #     print("Sell failed")
                # print(json.dumps(bft.withdraw('mastercoin', str(bf_usd_available), '16jyBXTmP2t21deSZJDT65vLJLsANqbYtL')))
                # print(json.dumps(bft.get_deposit_withdraw_history('mastercoin')))
            except Exception as ex:
                print(ex.message)
            time.sleep(config.time_to_sleep)
    except Exception as ex:
        raise ex
