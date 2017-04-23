from __future__ import print_function
import config
import polo
import btfx
import btrx

#p = polo.poloniex(config.POLO.APIKey, config.POLO.Secret)
#print(p.returnTicker())

b = btfx.Client()
print(b.ticker('btcusd'))

br = btrx.Bittrex(config.BTRX.Key,config.BTRX.Secret)
#print(br.get_markets())
print(br.get_ticker('USDT-BTC'))
