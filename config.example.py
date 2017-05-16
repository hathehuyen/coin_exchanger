class POLO:
    def __init__(self):
        pass
    APIKey = ""
    Secret = ""
    maker_fee = 0.0015
    taker_fee = 0.0025
    withdraw_fee = {
        "BTC": 0.0001,
        "ETC": 0.01,
        "ETH": 0.01,
        "USDT": 0.5
    }



class BTFX:
    def __init__(self):
        pass
    Key = ""
    Secret = ""
    maker_fee = 0.001
    taker_fee = 0.002
    wallet_adress = {
        "BTC": "",
        "USDT": ""
    }
    withdraw_fee = {
        "BTC": 0.0002,
        "USDT": 0.1
    }


class BTRX:
    def __init__(self):
        pass
    Key = ""
    Secret = ""
    wallet_adress = {
        "BTC": "",
        "USDT": ""
    }
    taker_fee = 0.0025
    withdraw_fee = {
        "BTC": 0.0002,
        "USDT": 0.1
    }

min_rate_per_exchange = 0.05