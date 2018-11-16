from pprint import pprint
from bitmax import WebSocketClient
from bitmax.utils import uuid32

class TradeBot(WebSocketClient):

  def initialize(self):
    self.orders = {}  # coid => symbol
    self.default_messages = {'depth', 'marketTrades'}

  def on_message(self, msg):
    if msg['m'] in self.default_messages:
      print(msg)
      return self.on_default_message(msg)
    print(f"unhandled message: {msg}")

client = TradeBot(
  "ETH/BTC",
  "https://bitmax.io",
  "",
  ""
)

res = client.user_info()
pprint(res)

client.group = res['accountGroup']

client.start()
