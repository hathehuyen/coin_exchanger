from __future__ import print_function
import config
import polo
import btfx

# p = polo.poloniex(config.POLO_APIKey, config.POLO_Secret)
b = btfx.Client()
# print(p.returnTicker())
print(b.ticker('btcusd'))
