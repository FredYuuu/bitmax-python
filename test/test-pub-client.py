from pprint import pprint
from bitmax import PublicClient

client = PublicClient("https://bitmax.io")

res = client.get_products()
pprint(res)

res = client.get_assets()
pprint(res)

res = client.get_quote("ETH/BTC")
pprint(res)

res = client.get_depth("ETH/BTC")
pprint(res)

res = client.get_ticker()
pprint(res)

res = client.get_ticker("ETH/BTC")
pprint(res)

res = client.get_trades("ETH/BTC", 3)
pprint(res)


res = client.get_quote("LFT/BTC")
pprint(res)
