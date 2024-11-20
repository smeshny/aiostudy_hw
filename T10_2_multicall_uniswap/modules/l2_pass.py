import asyncio

from eth_typing import HexStr

from client import Client
from config import CONTRACTS_PER_CHAIN, L2PASS_NFT_ABI


class L2Pass:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.contract = self.client.w3.eth.contract(
            address=CONTRACTS_PER_CHAIN[self.client.network.name]['L2PASS_NFT'],
            abi=L2PASS_NFT_ABI
        )

    async def get_mint_price(self) -> int:
        return await self.contract.functions.mintPrice().call()

    async def mint(self, nft_quantity: int = 1):
        mint_price_wei = await self.get_mint_price()

        total_price_wei = int(mint_price_wei * nft_quantity)
        total_price_ether = self.client.w3.from_wei(total_price_wei, 'ether')
        
        print(f"Start minting {nft_quantity} L2PASS nft's, mint price: {total_price_ether} ETH")
        try:
            tx_params = (await self.client.prepare_transaction()) | {
                'value': total_price_wei,
            }
            
            transaction = await self.contract.functions.mint(nft_quantity).build_transaction(tx_params)
            
            return await self.client.send_transaction(transaction)
        except Exception as error:
            if 'insufficient funds for transfer' in str(error):
                raise RuntimeError("You don't have enough funds for mint NFTs")
            else:
                raise error
