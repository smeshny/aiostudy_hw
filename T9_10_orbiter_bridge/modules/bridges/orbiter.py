import asyncio
import json

from custom_logger import logger
from client import Client
from networks import Network
from config import TOKENS_PER_CHAIN


class Orbiter:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.native_token = self.client.network.token

    async def get_bridge_data(
        self, src_token_name: str, src_chain: Network, dst_token_name: str, dst_chain: Network
        ):
        url = "https://api.orbiter.finance/sdk/routers/v2"
        orbiter_routers_response = await self.client.make_request(method='GET', url=url)
        
        orbiter_line = f"{src_chain.chain_id}/{dst_chain.chain_id}-{src_token_name}/{dst_token_name}"
        
        for router_data in orbiter_routers_response.get("result", []):
            if router_data.get("line") == orbiter_line:
                return router_data
            
        raise RuntimeError(f"Orbiter router not found for direction: "
                           f"{src_chain.name}/{dst_chain.name}-{src_token_name}/{dst_token_name}")

    async def get_transaction_status_from_orbiter(self, src_chain: Network, dst_chain: Network, tx_hash: str):
        url = f"https://api.orbiter.finance/sdk/transaction/status/{tx_hash}"
    
        max_time_to_wait = 360
        time_spent = 0
        while time_spent < max_time_to_wait:
            try:
                orbiter_tx_response = await self.client.make_request(method='GET', url=url)
                if orbiter_tx_response.get("status") == "success":
                    logger.success(f"Orbiter bridge transaction completed successfully!")
                    logger.success(f"{dst_chain.name} tx: "
                                f"{dst_chain.explorer}tx/{orbiter_tx_response['result']['targetId']}")
                    logger.success(f"Recieved on {dst_chain.name}: {orbiter_tx_response['result']['targetAmount']} "
                                f"{orbiter_tx_response['result']['targetSymbol']}")
                    return
            except Exception as error:
                if 'object is not subscriptable' in str(error):
                    logger.warning(f"Waiting for processing transaction on {dst_chain.name}...")
                else:
                    raise error
            await asyncio.sleep(15)
            time_spent += 15
        raise RuntimeError(f"Orbiter bridge transaction {src_chain.explorer}tx/{tx_hash} from {src_chain.name} to "
                           f"{dst_chain.name} is not recieved after {max_time_to_wait} seconds")

    async def bridge(
        self, 
        src_token_name: str, 
        src_chain: str,
        dst_token_name: str, 
        dst_chain: str,
        amount_to_bridge_ether: float
        ):
        bridge_data = await self.get_bridge_data(src_token_name, src_chain, dst_token_name, dst_chain)
        
        if bridge_data.get("state") != "available":
            raise RuntimeError(f"Orbiter bridge is not available for direction: "
                               f"{src_chain.name}/{dst_chain.name}-{src_token_name}/{dst_token_name}")
        if bridge_data.get("endpointContract") != None:
            raise RuntimeError(f"Orbiter data has additional endpoint smart contract, this is not supported yet")
        if float(bridge_data.get("maxAmt")) < amount_to_bridge_ether:
            raise RuntimeError(f"Orbiter bridge max amount is less than the amount to bridge: "
                               f"{bridge_data.get('maxAmt')} < {amount_to_bridge_ether}")
        if float(bridge_data.get("minAmt")) > amount_to_bridge_ether:
            raise RuntimeError(f"Orbiter bridge min amount is greater than the amount to bridge: "
                               f"{bridge_data.get('minAmt')} > {amount_to_bridge_ether:.6f}")
        
        bridge_fee_percent = float(bridge_data.get("tradeFee"))
        bridge_fee_amount = amount_to_bridge_ether * bridge_fee_percent
        bidge_withholding_fee_ether = float(bridge_data.get("withholdingFee"))
        total_fee_ether = bridge_fee_amount + bidge_withholding_fee_ether
        
        logger.info(f"Start bridging {amount_to_bridge_ether} {src_token_name} {src_chain.name} -> "
                    f"{dst_token_name} {dst_chain.name}")
        logger.info(f"Total fee for this direction: {total_fee_ether:.6f} {src_token_name}")

        src_token_address = TOKENS_PER_CHAIN[src_chain.name][src_token_name]
        src_token_decimals = await self.client.get_decimals(token_address=src_token_address)
        amount_to_bridge_wei = self.client.to_wei(amount_to_bridge_ether, src_token_decimals)
        
        orbiter_vc_wei = int(bridge_data.get("vc"))
        final_sum_wei = int(round(amount_to_bridge_wei, -4) + orbiter_vc_wei)

        orbiter_maker_address = self.client.w3.to_checksum_address(bridge_data.get("endpoint"))

        try:
            if src_token_name != self.native_token:
                token_contract = self.client.get_contract(src_token_address)
                transaction = await token_contract.functions.transfer(
                    orbiter_maker_address, 
                    final_sum_wei
                ).build_transaction(await self.client.prepare_transaction())
            else:
                transaction = (await self.client.prepare_transaction(value=final_sum_wei)) | {
                    'to': orbiter_maker_address
                }
                
            _, tx_hash = (await self.client.send_transaction(transaction))
            await self.get_transaction_status_from_orbiter(src_chain, dst_chain, tx_hash)
        except Exception as error:
            logger.error(f'{error}')
