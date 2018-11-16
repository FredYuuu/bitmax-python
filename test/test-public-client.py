import os
from bitmax import PublicClient


def test_get_products():
  client = PublicClient("https://bitmax.io")
  res = client.get_products()
  assert isinstance(res, list), "get_products should return a list object"
  assert len(res) > 0, "get_products should return non-empty list"


def test_get_assets():
  client = PublicClient("https://bitmax.io")
  res = client.get_assets()
  assert isinstance(res, list), "get_assets should return a list object"
  assert len(res) > 0, "get_assets should return non-empty list"

