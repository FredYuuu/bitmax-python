import click
from random import random
from time import sleep
from bitmax import *

@click.command()
@click.option("-i", type=int)
def run(i=0):
	apiKey, secret = [
		('', ''),
		('', ''),
	][i]

	client = AuthenticatedClient("https://bitmax.io", apiKey, secret)
	res = client.user_info()
	client.group = res['accountGroup']

	while True:

		prc = round(0.01 + random() * 0.09, 2)
		qty = round(0.5 + random() * 0.5, 2)

		if random() < 0.5:
			print(f"placing buy  order - {i}")
			res = client.place_new_order("ETH/BTC", prc, qty, "buy")
		else:
			print(f"placing sell order - {i}")
			res = client.place_new_order("ETH/BTC", prc, qty, "sell")
		sleep(5)

		print(f"canceling all orders - {i}")
		client.cancel_all()

		sleep(5)

if __name__ == '__main__':
	run()
