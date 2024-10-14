import networks

PRIVATE_KEY: str = '' # your private key

NETWORK_TO_WORK: networks.Network = networks.ArbitrumRPC #choose your network from networks.py
TOKEN_TO_SEND: str = 'USDC.e'
TO_ADDRESS: str = '' # address to send
VALUE_TO_SEND: float | None = 0.01 # value to send in ether | If None, all balance will be sent

UNLIMITED_APPROVE = False # if True, the contract will be approved for spending unlimited amount of tokens

GAS_PRICE_MULTIPLIER = 1.3
GAS_LIMIT_MULTIPLIER = 1.5
