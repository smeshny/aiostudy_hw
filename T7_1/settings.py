import networks


NETWORK_TO_WORK: networks.Network = networks.OptimismRPC #choose your network from networks.py
PRIVATE_KEY: str = '' # your private key
TO_ADDRESS: str = '' # address to send
VALUE_TO_SEND: float = 0.0000084 # value to send in ETH

GAS_PRICE_MULTIPLIER = 1.3
GAS_LIMIT_MULTIPLIER = 1.5