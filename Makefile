key ?= free_key
secret ?= free_secret

clean:
	find . -name "*.py[c|o]" -o -name __pycache__ -exec rm -rf {} \+


