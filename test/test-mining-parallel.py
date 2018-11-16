from random import random
from time import sleep
from bitmax import *
from multiprocessing import Pool

def run(i):
    apiKey, secret = [
    	('', ''),
    	('', ''),
    ][i]

    client = AuthenticatedClient("https://bitmax.io", apiKey, secret)
    res = client.user_info()
    client.group = res['accountGroup']

    side = "buy"

    while True:

        prc = round(0.01 + random() * 0.09, 2)
        qty = round(0.5 + random() * 0.5, 2)

        if random() < 0.5:
            print(f"placing buy  order - {i}")
            if side == 'buy':
                client.cancel_all()
                sleep(10 + random() * 100)
            res = client.place_new_order("ETH/BTC", prc, qty, "buy")
            side = "buy"
        else:
            print(f"placing sell order - {i}")
            if side == 'sell':
                client.cancel_all()
                sleep(10 + random() * 100)
            res = client.place_new_order("ETH/BTC", prc, qty, "sell")
            side = "sell"
        sleep(10 + random() * 100)


if __name__ == '__main__':
    p = Pool(5)
    p.map(run, [0, 1, 2, 3, 4])
