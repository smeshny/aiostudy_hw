import asyncio
from typing import Tuple

from eth_abi import abi

from custom_logger import logger
from client import Client
from networks import Network
from config import (TOKENS_PER_CHAIN, 
                    CONTRACTS_PER_CHAIN, 
                    STARGATE_V2_ENDPOINT_ID, 
                    STARGATE_V2_POOLNATIVE_ABI, 
                    STARGATE_V2_POOLUSDC_ABI)


class StargateV2:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.native_token = self.client.network.token
        self.pool_native_address = CONTRACTS_PER_CHAIN[self.client.network.name]["STARTGATE_V2_POOLNATIVE"]
        self.pool_native_contract = self.client.get_contract(
            contract_address=self.pool_native_address, abi=STARGATE_V2_POOLNATIVE_ABI
            )
        self.pool_usdc_address = CONTRACTS_PER_CHAIN[self.client.network.name]["STARGATE_V2_POOLUSDC"]
        self.pool_usdc_contract = self.client.get_contract(
            contract_address=self.pool_usdc_address, abi=STARGATE_V2_POOLUSDC_ABI
            )
    
    async def get_bridge_tx_data(
        self, src_token_name: str, dst_chain: Network, amount_to_bridge_wei: int, bridge_mode: str, slippage: float
        ) -> Tuple[int, Tuple, Tuple]:
        dst_chain_stargate_endpoint_id = STARGATE_V2_ENDPOINT_ID[dst_chain.name]

        send_param = (
            dst_chain_stargate_endpoint_id, # Destination endpoint ID
            abi.encode(['address'], [self.client.address]), # Recipient address bytes32
            amount_to_bridge_wei, # Amount to send in local decimals
            int(amount_to_bridge_wei * (1 - slippage / 100)), # Minimum amount to send in local decimals.
            "0x", # Additional options supplied by the caller to be used in the LayerZero message.
            "0x", # The composed message for the send() operation.
            "0x01" if bridge_mode == "BUS" else "0x" # The OFT command to be executed
        )

        contract = await self.get_stargate_contract(src_token_name)
        try:
            message_fee = await contract.functions.quoteSend(send_param, False).call()
        except Exception as error:
            raise RuntimeError(f"Error getting bridge tx data: {error}")
        
        total_to_pay_wei = message_fee[0] + amount_to_bridge_wei
        return total_to_pay_wei, send_param, message_fee
    
    async def get_stargate_contract(self, src_token_name: str):
        if src_token_name == "ETH":
            return self.pool_native_contract
        elif src_token_name == "USDC":
            return self.pool_usdc_contract
        else:
            raise RuntimeError(f"You try to bridge unsupported token: {src_token_name}! "
                               f"Only ETH and USDC are supported")
    
    async def get_bridge_status_from_l0_api(self, src_chain: Network, dst_chain: Network, tx_hash: str) -> None:
        url = f'https://api-mainnet.layerzero-scan.com/tx/{tx_hash}'

        max_time_to_wait = 360
        time_spent = 0
        while time_spent < max_time_to_wait:
            try:
                lz_tx_response = await self.client.make_request(method='GET', url=url)
                if lz_tx_response.get('messages') and "dstTxHash" in lz_tx_response["messages"][0]:
                    logger.success(f"Stargate V2 bridge transaction completed successfully!")
                    logger.success(f"{dst_chain.name} tx: "
                                f"{dst_chain.explorer}tx/{lz_tx_response['messages'][0]['dstTxHash']}")
                    return
            except Exception as error:
                raise error
            await asyncio.sleep(15)
            time_spent += 15
            logger.warning(f"Waiting {max_time_to_wait}s. for processing transaction on {dst_chain.name}... "
                           f"Time spent: {time_spent}s.")
        raise RuntimeError(f"Stargate V2 bridge transaction {src_chain.explorer}tx/{tx_hash} from {src_chain.name} to "
                           f"{dst_chain.name} is not recieved after {max_time_to_wait} seconds")
    
    async def bridge(
        self, 
        src_token_name: str, src_chain: Network, 
        dst_token_name: str, dst_chain: Network, 
        amount_to_bridge_ether: float, 
        bridge_mode: str,
        slippage: float
        ) -> None:
        
        src_token_decimals = await self.client.get_decimals(token_name=src_token_name)
        amount_to_bridge_wei = self.client.to_wei(amount_to_bridge_ether, src_token_decimals)

        total_to_pay_wei, send_param, message_fee = await self.get_bridge_tx_data(
            src_token_name, dst_chain, amount_to_bridge_wei, bridge_mode, slippage
            )

        bridge_fee_wei = message_fee[0]
        bridge_fee_ether = self.client.from_wei(bridge_fee_wei)
        
        logger.info(
            f"Starting bridge {amount_to_bridge_ether:.6f} {src_token_name} {src_chain.name} -> "
            f"{dst_token_name} {dst_chain.name}. "
            f"Bridge mode: {bridge_mode}. Fee: {bridge_fee_ether:.6f} {self.native_token}.")
        
        contract = await self.get_stargate_contract(src_token_name)

        try:
            if src_token_name != self.native_token:
                await self.client.check_for_approved(
                token_address=TOKENS_PER_CHAIN[src_chain.name][src_token_name], 
                spender_address=contract.address, 
                amount_in_wei=amount_to_bridge_wei
                )
            
            tx_params = (await self.client.prepare_transaction()) | {
                'value': total_to_pay_wei if src_token_name == self.native_token else bridge_fee_wei,
            }
            transaction = await contract.functions.send(
                send_param, 
                message_fee, 
                self.client.address
                ).build_transaction(tx_params)
            _, tx_hash = await self.client.send_transaction(transaction)
            await self.get_bridge_status_from_l0_api(src_chain, dst_chain, tx_hash)
        except Exception as error:
            raise RuntimeError(f"Error sending bridge tx: {error}")
