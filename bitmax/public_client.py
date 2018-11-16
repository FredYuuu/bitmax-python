import requests
import json
from .utils import *


class PublicClient(object):

  def __init__(self, api_url=None):
    self._api_url = api_url

  @property
  def api_url(self):
    return self._api_url

  def get_products(self):
    """function:: get_products()

    Get product info of a symbol
    :rtype: list
    """
    url = f"{self._api_url}/api/v1/products"
    return GET(url)

  def get_assets(self):
    """function:: get_products()
    
    Get all products listed on the exchange

    :rtype: None or list of dict
    """
    url = f"{self._api_url}/api/v1/assets"
    return GET(url)
    
  def get_quote(self, symbol):
    url = f"{self._api_url}/api/v1/quote"
    return GET(url, params=dict(symbol=symbol.replace("/", "-")))

  def get_depth(self, symbol, n=10):
    url = f"{self._api_url}/api/v1/depth"
    return GET(url, params=dict(symbol=symbol.replace("/", "-"), n=n))

  def get_ticker(self, symbol=None):
    url = f"{self._api_url}/api/v1/ticker/24hr"
    if symbol is None:
      return GET(url)
    else:
      return GET(url, params=dict(symbol=symbol.replace("/", "-")))

  def get_trades(self, symbol, n=10):
    url = f"{self._api_url}/api/v1/trades"
    return GET(url, params=dict(symbol=symbol.replace("/", "-"), n=n))
