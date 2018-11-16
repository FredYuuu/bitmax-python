import json
import time 
from pprint import pprint
from threading import Thread
from websocket import create_connection
from os.path import join as path_join

from . import AuthenticatedClient
from .utils import *

class WebSocketClient(AuthenticatedClient):

  def __init__(self, symbol, ws_url, api_key=None, secret=None, depths=20, trades=20, *args, **kwargs):
    super().__init__(
      api_url = ws_url.replace("ws://", "http://").replace("https://", "http://"), 
      api_key = api_key,
      secret = secret, 
      *args, 
      **kwargs)
    self._symbol = symbol.replace('/', '-')
    self._ws = None
    self._base_url = ws_url.replace("http://", "ws://").replace("https://", "wss://")
    self._num_depths = max(1, int(depths))
    self._num_trades = max(1, int(trades))
    
  @property
  def ws_url(self):
    return path_join(self._base_url, str(self._group), "api/stream", self._symbol)
  
  def start(self):
    def loop():
      self._connect()
      self._listen()
      self._disconnect()
    self._running = True
    self.initialize()
    self.thread = Thread(target=loop)
    self.thread.start()

  @property
  def ready(self):
    return self._ws is not None
  
  def initialize(self):
    pass

  def on_close(self):
    pass

  def on_default_message(self, msg):
    pass

  def send(self, msg):
    self._ws.send(msg)

  def on_message(self, msg):
    self.on_default_message(msg)

  def _connect(self):
    ts = utc_timestamp()
    headers = make_auth_header(ts, "api/stream", self.api_key, self.secret)
    print(f"connecting to websocket server: {self.ws_url}")
    self._ws = create_connection(self.ws_url, header=headers)

  def _disconnect(self):
    try:
      if self._ws:
        self._ws.close()
    except WebSocketConnectionClosedException as e:
      pass
    self.on_close()

  def _listen(self):
    subscribe = """{
        "messageType":         "subscribe",
        "marketDepthLevel":    %d,
        "recentTradeMaxCount": %d
      }
    """ % (self._num_depths, self._num_trades)
    print("Sending subscribe message ...")
    self._ws.send(subscribe)
  
    while self._running:
      try:
        start_t = 0
        if time.time() - start_t >= 30:
            # Set a 30 second ping to keep connection alive
            self._ws.ping("keepalive")
            start_t = time.time()
        data = self._ws.recv()
        try: 
          msg = json.loads(data)
        except: 
          raise f"Failed to parse message a json: {data}"
      except ValueError as e:
        print("ValueError as e")
        self.on_error(e)
      except Exception as e:
        print("Exception as e")
        self.on_error(e)
      else:
          self.on_message(msg)

  def on_error(self, e):
    print("Error" + str(e))
    self._running = False

  def place_new_order_ws(self, symbol, price, quantity, side):
    """function:: place_new_order(symbol, price, quantity, side)

    Place a new order via the WebSocket API

    :type symbol: string
   `:type price: float 
    :type quantity: float
   `:param side: buy or sell
   `:rtype: None or dict 
    """
    msg = json.dumps(
      dict(
        messageType = "newOrderRequest", 
        coid = uuid32(),
        time = utc_timestamp(),
        symbol = symbol.replace("-", "/"),
        orderPrice = str(price),
        orderQty = str(quantity),
        orderType = "limit",
        side = side
      ))
    self._ws.send(msg)

  def cancel_order_ws(self, symbol, coid):
    """function:: cancel_order(symbol, coid) 

    Cancel an existing order via the WebSocket API

    :type symbol: string
   `:param coid: the coid of the order to be cancel
   `:type coid: string
   `:rtype: None or dict
    """
    msg = json.dumps(
      dict(
        messageType = "cancelOrderRequest", 
        time = utc_timestamp(),
        coid = uuid32(),
        origCoid = coid,   
        symbol = symbol.replace("-", "/"),
      ))
    print(f"cancel order: {msg}")
