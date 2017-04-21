from __future__ import print_function
import config
import polo
import btfx
import btrx

#p = polo.poloniex(config.POLO.APIKey, config.POLO.Secret)
b = btfx.Client()
#print(p.returnTicker())
print(b.ticker('btcusd'))
br = btrx.Bittrex("api","secret")
print(br.get_ticker('btc_usd'))