import os

from dotenv import load_dotenv

import networks


# NETWORK_TO_WORK: networks.Network = networks.LineaRPC # choose your network from networks.py

UNLIMITED_APPROVE = False # if True, the contract will be approved for spending unlimited amount of tokens

GAS_PRICE_MULTIPLIER = 1.3
GAS_LIMIT_MULTIPLIER = 1.5

load_dotenv()

PRIVATE_KEY = os.getenv('PRIVATE_KEY')
PROXY = os.getenv('PROXY')
CAPMONSTER_API_KEY = os.getenv('CAPMONSTER_API_KEY')

