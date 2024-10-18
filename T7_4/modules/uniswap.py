import asyncio
import time

from eth_account.datastructures import SignedMessage

from client import Client
from settings import UNLIMITED_APPROVE


class Uniswap:
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    async def sign_erc20_swap_permit(
        self, erc20_address_to_spend: str, spender_contract_address: str, amount_ether: float | int = 0
        ) -> SignedMessage:
        """
        https://blog.uniswap.org/permit2-integration-guide
        First, in order to get the signature for a PermitSingle, you'll need the next valid nonce, which you can get using the SDK.

        import { AllowanceProvider, PERMIT2_ADDRESS } from '@uniswap/Permit2-sdk'

        const allowanceProvider = new AllowanceProvider(ethersProvider, PERMIT2_ADDRESS)
        const { amount: permitAmount, expiration, nonce } = allowanceProvider.getAllowanceData(user, token, ROUTER_ADDRESS);

        // You may also check amount/expiration here to see if you are already permitted -
        // you may not need to generate a new signature.
        """
        nonce = 0
        
        if UNLIMITED_APPROVE:
            amount = 2 ** 256 - 1
        else:
            amount = self.client.w3.to_wei(amount_ether, 'ether')

        permit_data = {
            "types": {
                "PermitSingle": [
                    {"name": "details", "type": "PermitDetails"},
                    {"name": "spender", "type": "address"},
                    {"name": "sigDeadline", "type": "uint256"},
                ],
                "PermitDetails": [
                    {"name": "token", "type": "address"},
                    {"name": "amount", "type": "uint160"},
                    {"name": "expiration", "type": "uint48"},
                    {"name": "nonce", "type": "uint48"},
                ],
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
            },
            "primaryType": "PermitSingle",
            "domain": {
                "name": "Permit2",
                "chainId": self.client.network.chain_id,
                "verifyingContract": "0x000000000022D473030F116dDEE9F6B43aC78BA3", #canonical Permit2 contract
            },
            "message": {
                "details": {
                    "token": erc20_address_to_spend,
                    "amount": amount, 
                    "expiration": int(time.time() + 60 * 60 * 24 * 30), #30 days https://blog.uniswap.org/permit2-integration-guide
                    "nonce": nonce, #nonce is the next valid nonce for the token and spender
                },
                "spender": spender_contract_address,
                "sigDeadline": int(time.time() + 60 * 60 * 30), #30 minutes https://blog.uniswap.org/permit2-integration-guide
            },
        }

        signed_message: SignedMessage = await self.client.custom_sign_message(
            data_to_sign=permit_data, eip_712_data=True
            )
        
        if await self.client.verify_signature(
            data_to_sign=permit_data, 
            signed_message=signed_message, 
            eip_712_data=True
            ):
            print("Uniswap approval signature verification passed")
            return signed_message
        else:
            raise RuntimeError("Signature verification failed")
