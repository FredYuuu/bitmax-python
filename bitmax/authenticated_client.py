from .public_client import PublicClient
from .utils import *
from pprint import pprint


class AuthenticatedClient(PublicClient):

  def __init__(self, api_url, api_key, secret, *args, **kwargs):
    super().__init__(api_url, *args, **kwargs)
    self._api_key = api_key
    self._secret = secret
    self._group = None

  @property
  def api_key(self):
    return self._api_key

  @property
  def group(self):
    return self._group

  @group.setter
  def group(self, grp):
    self._group = str(grp)

  @property
  def secret(self):
    return self._secret

  def user_info(self):
    """function:: cancel_all()

    Cancel all outstanding orders
    """
    ts = utc_timestamp()
    headers = make_auth_header(ts, "user/info", self._api_key, self._secret)
    return GET(f"{self.api_url}/api/v1/user/info", headers=headers)

  def get_balances(self):
    """function:: get_balances()

    Get current balance of each asset.

    :rtype: None or list of dict
    """
    api_path = "balance"
    ts = utc_timestamp()
    headers = make_auth_header(ts, api_path, self._api_key, self._secret)
    return GET(f"{self.api_url}/{self._group}/api/v1/balance", headers=headers)

  def get_balance(self, asset):
    """function:: get_balances()

    Get current balance of each asset.

    :rtype: None or list of dict
    """
    if asset == '':
      raise ValueError("Invalid asset")

    api_path = "balance"
    ts = utc_timestamp()
    headers = make_auth_header(ts, api_path, self._api_key, self._secret)
    return GET(f"{self.api_url}/{self._group}/api/v1/balance/{asset}", headers=headers)

  def get_open_orders(self, symbol=None):
    """function:: get_balances()

    Get current balance of each asset.

    :rtype: None or list of dict
    """
    api_path = "order/open"
    ts = utc_timestamp()
    headers = make_auth_header(ts, api_path, self._api_key, self._secret)
    if symbol is None:
      return GET(f"{self.api_url}/{self._group}/api/v1/order/open", headers=headers)
    else:
      return GET(f"{self.api_url}/{self._group}/api/v1/order/open", headers=headers, params=dict(symbol=symbol))

  def get_order_history(self, symbol=None, start_time=0, end_time=2500000000000, n=50):
    """function:: get_order_history()

    Get current balance of each asset.

    :rtype: None or list of dict
    """
    api_path = "order/history"
    ts = utc_timestamp()
    headers = make_auth_header(ts, api_path, self._api_key, self._secret)
    if symbol is None:
      return GET(f"{self.api_url}/{self._group}/api/v1/order/history", headers=headers, params=dict(startTime=start_time, endTime=end_time, n=n))
    else:
      return GET(f"{self.api_url}/{self._group}/api/v1/order/history", headers=headers, params=dict(symbol=symbol, startTime=start_time, endTime=end_time, n=n))

  def get_order(self, coid):
    api_path = "order"
    ts = utc_timestamp()
    headers = make_auth_header(ts, api_path, self._api_key, self._secret)
    return GET(f"{self.api_url}/{self._group}/api/v1/order/{coid}", headers=headers)

  def place_new_order(self, symbol, price, quantity, side):
    """function:: place_new_order(symbol, price, quantity, side)

    Place a new order.

    :type symbol: string
    :type price: float
    :type quantity: float
    :param side: buy or sell
    :rtype: None or dict
    """
    ts = utc_timestamp()
    coid = uuid32()
    headers = make_auth_header(ts, "order", self._api_key, self._secret, coid)
    order = dict(
        coid       = coid,
        time       = ts,
        symbol     = symbol.replace("-", "/"),
        orderPrice = str(price),
        orderQty   = str(quantity),
        orderType  = "limit",
        side       = side.lower()
    )
    return POST(f"{self.api_url}/{self._group}/api/v1/order", json=order, headers=headers)

  def batch_place_orders(self, orders):
    """function:: place_new_order(symbol, price, quantity, side)

    Place multiple orders.
    """
    ts = utc_timestamp()
    req = [dict(
        coid       = uuid32(),
        time       = ts,
        symbol     = symbol.replace("-", "/"),
        orderPrice = str(price),
        orderQty   = str(quantity),
        orderType  = "limit",
        side       = side.lower()
    ) for (symbol, price, quantity, side) in orders]

    coids = "+".join([r['coid'] for r in req])
    headers = make_auth_header(ts, "order/batch", self._api_key, self._secret, coids)

    return POST(f"{self.api_url}/{self._group}/api/v1/order/batch", json={"orders": req}, headers=headers)

  def cancel_order(self, symbol, origCoid):
    """function:: cancel_order(symbol, origCoid)

    Cancel an existing order.

    :type symbol: string
    :param coid: the coid of the order to be cancel
    :type coid: string
    :rtype: None or dict
    """
    ts = utc_timestamp()
    coid = uuid32()
    headers = make_auth_header(ts, "order", self._api_key, self._secret, coid)
    order = dict(
        coid     = coid,
        origCoid = origCoid,
        time     = ts,
        symbol   = symbol.replace("-", "/"),
    )
    return DELETE(f"{self.api_url}/{self._group}/api/v1/order", json=order, headers=headers)

  def batch_cancel_orders(self, orders):
    """function:: place_new_order(symbol, price, quantity, side)

    Cancel multiple orders.
    """
    ts = utc_timestamp()
    req = [dict(
        coid     = uuid32(),
        origCoid = origCoid,
        time     = ts,
        symbol   = symbol.replace("-", "/"),
    ) for symbol, origCoid in orders]

    coids = "+".join([r['coid'] for r in req])
    headers = make_auth_header(ts, "order/batch", self._api_key, self._secret, coids)

    return DELETE(f"{self.api_url}/{self._group}/api/v1/order/batch", json={"orders": req}, headers=headers)

  def cancel_all(self):
    ts = utc_timestamp()
    headers = make_auth_header(ts, "order/all", self._api_key, self._secret)
    return DELETE(f"{self.api_url}/{self._group}/api/v1/order/all", headers=headers)

  def get_fills(self, coid):
    ts = utc_timestamp()
    headers = make_auth_header(ts, "order/fills", self._api_key, self._secret)
    return GET(f"{self.api_url}/{self._group}/api/v1/order/fills/{coid}", headers=headers)

  def get_deposit(self):
    ts = utc_timestamp()
    headers = make_auth_header(ts, "transaction", self._api_key, self._secret)
    print(headers)
    return GET(f"{self.api_url}/{self._group}/api/v1/transaction?page=1&pageSize=10", headers=headers)

