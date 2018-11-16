import json 
import requests
from datetime import datetime
import hmac, hashlib, base64
import random, string    


def uuid32():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))


def utc_timestamp():
  tm = datetime.utcnow().timestamp()
  return int(tm * 1e3)


def make_auth_header(timestamp, api_path, api_key, secret, coid=None): 
  # convert timestamp to string   
  if isinstance(timestamp, bytes):
    timestamp = timestamp.decode("utf-8")
  elif isinstance(timestamp, int):
    timestamp = str(timestamp)

  if coid is None:
    msg = bytearray(f"{timestamp}+{api_path}".encode("utf-8"))
  else:
    msg = bytearray(f"{timestamp}+{api_path}+{coid}".encode("utf-8"))

  hmac_key = base64.b64decode(secret)
  signature = hmac.new(hmac_key, msg, hashlib.sha256)
  signature_b64 = base64.b64encode(signature.digest()).decode("utf-8")  
  header = {
    "x-auth-key": api_key,
    "x-auth-signature": signature_b64,
    "x-auth-timestamp": timestamp,
  }

  # hmac_key = bytearray(secret.encode("utf-8"))  
  # signature = base64.b64encode(hmac.new(hmac_key, msg, digestmod=hashlib.sha256).digest())
  # header = {
  #   "x-auth-key": api_key,
  #   "x-auth-signature": signature.decode(),
  #   "x-auth-timestamp": timestamp,
  # }

  if coid is not None:
    header["x-auth-coid"] = coid

  return header


def GET(url, *args, **kwargs):
  try: 
    res = requests.get(url, *args, **kwargs)
    return __parse_response(res)
  except requests.exceptions.ConnectionError: 
    print(f"[WARN] Failed to connect {url}")
    return None
  except: 
    raise

def POST(url, *args, **kwargs):
  try: 
    res = requests.post(url, *args, **kwargs)
    return __parse_response(res)
  except requests.exceptions.ConnectionError: 
    print(f"[WARN] Failed to connect {url}")
    return None
  except: 
    raise

def DELETE(url, *args, **kwargs):
  try: 
    res = requests.delete(url, *args, **kwargs)
    return __parse_response(res)
  except requests.exceptions.ConnectionError: 
    print(f"[WARN] Failed to connect {url}")
    return None
  except: 
    raise

def __parse_response(res):
  if res is None:
    return None 

  if res.status_code == 200:
    data = json.loads(res.text)
    return data
  else:
    print(f"request failed, error code = {res.status_code}")
    print(res.text)
