from pprint import pprint
from bitmax import AuthenticatedClient
from bitmax.utils import uuid32

# mm2@hdconsultingservice.io
client = AuthenticatedClient(
  "https://bitmax.io",
  "",
  ""
)

res = client.user_info()
pprint(res)

client.group = res['accountGroup']

res = client.place_new_order("ETH/BTC", "0.049", "1.0", "sell")
pprint(res)

