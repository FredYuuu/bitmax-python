from pprint import pprint
from bitmax import AuthenticatedClient
from bitmax.utils import uuid32

# mm2@hdconsultingservice.io
client = AuthenticatedClient(
  "http://bitmax.io",
  "",
  ""
)

res = client.user_info()
pprint(res)

client.group = res['accountGroup']

res = client.get_balances()
pprint(res)

res = client.get_balance("BTC")
pprint(res)

res = client.get_balance("ETH")
pprint(res)

res = client.get_open_orders()
pprint(res)

res = client.get_order_history()
pprint(res)

res = client.get_open_orders("ETH/BTC")
pprint(res)

res = client.place_new_order("ETH/BTC", 0.033, 10, "buy")
pprint(res)

coid = res['data']['coid']

# Place/Cancel Orders in Batch
res = client.batch_place_orders([
    ("ZIL/BTC", 0.1002, 200, "buy"),
    ("ZIL/BTC", 0.1003, 300, "buy"),
    ("ZIL/BTC", 0.1004, 400, "buy"),
    ("ZIL/BTC", 0.1005, 500, "sell"),
    ("ZIL/BTC", 0.1006, 600, "sell"),
    ("ZIL/BTC", 0.1007, 700, "sell"),
  ])
pprint(res)

res1 = client.batch_cancel_orders(res['data'])
pprint(res1)

res = client.cancel_order("ETH/BTC", "")
pprint(res)


res = client.get_order("")
pprint(res)

res = client.cancel_order("ETH/BTC", coid)
pprint(res)

res = client.get_fills("")
pprint(res)

res = client.cancel_all()
pprint(res)


res = client.get_quote("ETH/BTC")
ask = float(res['askPrice'])
order = client.place_new_order("ETH/BTC", ask, 0.1, 'sell')

client.get_order(order['data']['coid'])
order2 = client.cancel_order("ETH/BTC", order['data']['coid'])

client.get_order(order2['data']['coid'])
