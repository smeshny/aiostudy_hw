TOKENS_PER_CHAIN = {
    'Ethereum': {
        'ETH'               : '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        'WETH'              : '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        'USDC'              : '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
        'USDT'              : '0xdAC17F958D2ee523a2206206994597C13D831ec7',
    },
    "Avalanche": {
        'ETH'               : '0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB',
        'WETH.e'            : '0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB',
        'USDC'              : '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
        'USDC.e'            : '0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664',
        'USDT'              : '0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7',
    },
    "Arbitrum":{
        "ETH"               : "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "WETH"              : "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        'ARB'               : "0x912CE59144191C1204E64559FE8253a0e49E6548",
        'USDC'              : "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        'USDT'              : "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        'USDC.e'            : "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
        'DAI'               : "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
        'OX'                : "0xba0Dda8762C24dA9487f5FA026a9B64b695A07Ea"
    },
    'Arbitrum Nova':{
        "ETH"               : "0x722E8BdD2ce80A4422E880164f2079488e115365",
        "WETH"              : "0x722E8BdD2ce80A4422E880164f2079488e115365",
        "USDC"              : "0x750ba8b76187092B0D1E87E28daaf484d1b5273b",
        "DAI"               : "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"
    },
    'Blast':{
        "ETH"               : "0x4300000000000000000000000000000000000004",
        "WETH"              : "0x4300000000000000000000000000000000000004",
        "USDB"              : "0x4300000000000000000000000000000000000003"
    },
    'Zora':{
        "ETH"               : "0x4200000000000000000000000000000000000006",
        "WETH"              : "0x4200000000000000000000000000000000000006"
    },
    "Optimism":{
        "ETH"               : "0x4200000000000000000000000000000000000006",
        "WETH"              : "0x4200000000000000000000000000000000000006",
        "OP"                : "0x4200000000000000000000000000000000000042",
        "USDC"              : "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
        "USDT"              : "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
        "USDC.e"            : "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
        "DAI"               : "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"
    },
    "Polygon":{
        'MATIC'             : "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        'WMATIC'            : "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        'POL'               : "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        'WPOL'              : "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        'ETH'               : "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        'WETH'              : "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        'USDT'              : "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
        'USDC'              : "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
        'USDC.e'            : "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    },
    "Polygon zkEVM":{
        'ETH'               : "0x4F9A0e7FD2Bf6067db6994CF12E4495Df938E6e9",
        'WETH'              : "0x4F9A0e7FD2Bf6067db6994CF12E4495Df938E6e9",
        'USDC'              : "0xA8CE8aee21bC2A48a5EF670afCc9274C7bbbC035",
    },
    "zkSync": {
        "ETH"               : "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        "WETH"              : "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        "USDC"              : "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
        "USDT"              : "0x493257fD37EDB34451f62EDf8D2a0C418852bA4C",
        #"BUSD"              : "0x2039bb4116B4EFc145Ec4f0e2eA75012D6C0f181"
    },
    "Base":{
        "ETH"               : "0x4200000000000000000000000000000000000006",
        "WETH"              : "0x4200000000000000000000000000000000000006",
        "USDC"              : "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "USDC.e"            : "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",
    },
    "Linea":{
        "ETH"               : "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",
        "WETH"              : "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",
        "USDT"              : "0xA219439258ca9da29E9Cc4cE5596924745e12B93",
        "USDC"              : "0x176211869cA2b568f2A7D4EE941E073a821EE1ff",
    },
    "Scroll":{
        "ETH"               : "0x5300000000000000000000000000000000000004",
        "WETH"              : "0x5300000000000000000000000000000000000004",
        "USDT"              : "0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df",
        "USDC"              : "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4",
    },
    "BNB Chain":{
        "BNB"               : "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
        "USDT"              : "0x55d398326f99059fF775485246999027B3197955",
        "USDC"              : "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
    },
    "Manta":{
        "ETH"               : "0x0Dc808adcE2099A9F62AA87D9670745AbA741746",
        "WETH"              : "0x0Dc808adcE2099A9F62AA87D9670745AbA741746",
        "USDT"              : "0xf417F5A458eC102B90352F697D6e2Ac3A3d2851f",
        "USDC"              : "0xb73603C5d87fA094B7314C74ACE2e64D165016fb",
    },
    "Mode":{
        "ETH"               : "0x4200000000000000000000000000000000000006",
        "WETH"              : "0x4200000000000000000000000000000000000006",
        "USDT"              : "0xf0F161fDA2712DB8b566946122a5af183995e2eD",
        "USDC"              : "0xd988097fb8612cc24eeC14542bC03424c656005f",
    },
    "Gravity": {
        "G": '0xa4151B2B3e269645181dCcF2D426cE75fcbDeca9',
        "ETH": '0xf6f832466Cd6C21967E0D954109403f36Bc8ceaA',
    },
    "Taiko": {
        "ETH": '0xf6f832466Cd6C21967E0D954109403f36Bc8ceaA',
    },
}

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

CONTRACTS_PER_CHAIN = {
    "Arbitrum": {
        "UNISWAP_UNIVERSAL_ROUTER_4"    : "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "L2PASS_NFT"                    : "0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222",
        "UNISWAP_V2_ROUTER"             : "0x4752ba5DBc23f44D87826276BF6Fd6b1C372aD24",
        "UNISWAP_V2_FACTORY"            : "0xf1D7CC64Fb4452F05c498126312eBE29f30Fbcf9",
    },
    "Optimism": {
        "UNISWAP_V2_ROUTER"             : "0x4A7b5Da61326A6379179b40d00F57E5bbDC962c2",
        "UNISWAP_V2_FACTORY"            : "0x0c3c1c532F1e39EdF36BE9Fe0bE1410313E074Bf",
    },
    "BNB Chain": {
        "UNISWAP_V2_ROUTER"             : "0x4752ba5dbc23f44d87826276bf6fd6b1c372ad24",
        "UNISWAP_V2_FACTORY"            : "0x8909Dc15e40173Ff4699343b6eB8132c65e18eC6",
    },
    "Polygon": {
        "UNISWAP_V2_ROUTER"             : "0xedf6066a2b290C185783862C7F4776A2C8077AD1",
        "UNISWAP_V2_FACTORY"            : "0x9e5A52f57b3038F1B8EeE45F28b3C1967e22799C",
    },
}

ERC20_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "_name", "type": "string"},
            {"internalType": "string", "name": "_symbol", "type": "string"},
            {"internalType": "uint256", "name": "_initialSupply", "type": "uint256"},
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Approval",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"},
        ],
        "name": "decreaseAllowance",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "addedValue", "type": "uint256"},
        ],
        "name": "increaseAllowance",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint8", "name": "decimals_", "type": "uint8"}],
        "name": "setupDecimals",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "sender", "type": "address"},
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]

L2PASS_NFT_ABI = [{"inputs":[{"internalType":"uint256","name":"minGasToStore","type":"uint256"},{"internalType":"uint256","name":"defaultGasLimit","type":"uint256"},{"internalType":"address","name":"layerZeroEndpoint","type":"address"},{"internalType":"uint256","name":"startMintId","type":"uint256"},{"internalType":"uint256","name":"endMintId","type":"uint256"},{"internalType":"uint256","name":"mintPrice_","type":"uint256"},{"internalType":"uint256","name":"sendPrice_","type":"uint256"},{"internalType":"uint8","name":"chainId","type":"uint8"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"approved","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"operator","type":"address"},{"indexed":False,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"bytes32","name":"_hashedPayload","type":"bytes32"}],"name":"CreditCleared","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"bytes32","name":"_hashedPayload","type":"bytes32"},{"indexed":False,"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"CreditStored","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"indexed":False,"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"indexed":False,"internalType":"uint64","name":"_nonce","type":"uint64"},{"indexed":False,"internalType":"bytes","name":"_payload","type":"bytes"},{"indexed":False,"internalType":"bytes","name":"_reason","type":"bytes"}],"name":"MessageFailed","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"indexed":True,"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"indexed":True,"internalType":"address","name":"_toAddress","type":"address"},{"indexed":False,"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"}],"name":"ReceiveFromChain","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"referrer","type":"address"},{"indexed":False,"internalType":"address","name":"referral","type":"address"}],"name":"Referral","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"indexed":False,"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"indexed":False,"internalType":"uint64","name":"_nonce","type":"uint64"},{"indexed":False,"internalType":"bytes32","name":"_payloadHash","type":"bytes32"}],"name":"RetryMessageSuccess","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"indexed":True,"internalType":"address","name":"_from","type":"address"},{"indexed":True,"internalType":"bytes","name":"_toAddress","type":"bytes"},{"indexed":False,"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"}],"name":"SendToChain","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"indexed":False,"internalType":"uint256","name":"_dstChainIdToBatchLimit","type":"uint256"}],"name":"SetDstChainIdToBatchLimit","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"indexed":False,"internalType":"uint256","name":"_dstChainIdToTransferGas","type":"uint256"}],"name":"SetDstChainIdToTransferGas","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"indexed":False,"internalType":"uint16","name":"_type","type":"uint16"},{"indexed":False,"internalType":"uint256","name":"_minDstGas","type":"uint256"}],"name":"SetMinDstGas","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_minGasToTransferAndStore","type":"uint256"}],"name":"SetMinGasToTransferAndStore","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"precrime","type":"address"}],"name":"SetPrecrime","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint16","name":"_remoteChainId","type":"uint16"},{"indexed":False,"internalType":"bytes","name":"_path","type":"bytes"}],"name":"SetTrustedRemote","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint16","name":"_remoteChainId","type":"uint16"},{"indexed":False,"internalType":"bytes","name":"_remoteAddress","type":"bytes"}],"name":"SetTrustedRemoteAddress","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"DEFAULT_PAYLOAD_SIZE_LIMIT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"FUNCTION_TYPE_SEND","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimFunds","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"clearCredits","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"dstChainIdToBatchLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"dstChainIdToTransferGas","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"bytes","name":"_toAddress","type":"bytes"},{"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"},{"internalType":"bool","name":"_useZro","type":"bool"},{"internalType":"bytes","name":"_adapterParams","type":"bytes"}],"name":"estimateSendBatchFee","outputs":[{"internalType":"uint256","name":"nativeFee","type":"uint256"},{"internalType":"uint256","name":"zroFee","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"bytes","name":"_toAddress","type":"bytes"},{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"bool","name":"_useZro","type":"bool"},{"internalType":"bytes","name":"_adapterParams","type":"bytes"}],"name":"estimateSendFee","outputs":[{"internalType":"uint256","name":"nativeFee","type":"uint256"},{"internalType":"uint256","name":"zroFee","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"},{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"uint64","name":"","type":"uint64"}],"name":"failedMessages","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"}],"name":"forceResumeReceive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"},{"internalType":"uint16","name":"_chainId","type":"uint16"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"_configType","type":"uint256"}],"name":"getConfig","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_remoteChainId","type":"uint16"}],"name":"getTrustedRemoteAddress","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"getVisitedChains","outputs":[{"internalType":"uint8[]","name":"visitedChains","type":"uint8[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"}],"name":"isTrustedRemote","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lzEndpoint","outputs":[{"internalType":"contract ILayerZeroEndpoint","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint64","name":"_nonce","type":"uint64"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"lzReceive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"maxMintId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"metadataGenerator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"},{"internalType":"uint16","name":"","type":"uint16"}],"name":"minDstGasLookup","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"minGasToTransferAndStore","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"n","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"mintPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"n","type":"uint256"},{"internalType":"address","name":"referrer","type":"address"}],"name":"mintWithReferral","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"nextMintId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint64","name":"_nonce","type":"uint64"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"nonblockingLzReceive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"payloadSizeLimitLookup","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"precrime","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint64","name":"_nonce","type":"uint64"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"retryMessage","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"bytes","name":"_toAddress","type":"bytes"},{"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"},{"internalType":"address payable","name":"_refundAddress","type":"address"},{"internalType":"address","name":"_zroPaymentAddress","type":"address"},{"internalType":"bytes","name":"_adapterParams","type":"bytes"}],"name":"sendBatchFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"bytes","name":"_toAddress","type":"bytes"},{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"address payable","name":"_refundAddress","type":"address"},{"internalType":"address","name":"_zroPaymentAddress","type":"address"},{"internalType":"bytes","name":"_adapterParams","type":"bytes"}],"name":"sendFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"sendPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"},{"internalType":"uint16","name":"_chainId","type":"uint16"},{"internalType":"uint256","name":"_configType","type":"uint256"},{"internalType":"bytes","name":"_config","type":"bytes"}],"name":"setConfig","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_dstChainIdToBatchLimit","type":"uint256"}],"name":"setDstChainIdToBatchLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_dstChainIdToTransferGas","type":"uint256"}],"name":"setDstChainIdToTransferGas","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"metadataGenerator_","type":"address"}],"name":"setMetadataGenerator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint16","name":"_packetType","type":"uint16"},{"internalType":"uint256","name":"_minGas","type":"uint256"}],"name":"setMinDstGas","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_minGasToTransferAndStore","type":"uint256"}],"name":"setMinGasToTransferAndStore","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"mintPrice_","type":"uint256"}],"name":"setMintPrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_size","type":"uint256"}],"name":"setPayloadSizeLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_precrime","type":"address"}],"name":"setPrecrime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"}],"name":"setReceiveVersion","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"sendPrice_","type":"uint256"}],"name":"setSendPrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"}],"name":"setSendVersion","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_remoteChainId","type":"uint16"},{"internalType":"bytes","name":"_path","type":"bytes"}],"name":"setTrustedRemote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_remoteChainId","type":"uint16"},{"internalType":"bytes","name":"_remoteAddress","type":"bytes"}],"name":"setTrustedRemoteAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"storedCredits","outputs":[{"internalType":"uint16","name":"srcChainId","type":"uint16"},{"internalType":"address","name":"toAddress","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"},{"internalType":"bool","name":"creditsRemain","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"trustedRemoteLookup","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"visitedChainsMask","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]

ODOS_ROUTER_V2_ABI = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"sender","type":"address"},{"indexed":False,"internalType":"uint256","name":"inputAmount","type":"uint256"},{"indexed":False,"internalType":"address","name":"inputToken","type":"address"},{"indexed":False,"internalType":"uint256","name":"amountOut","type":"uint256"},{"indexed":False,"internalType":"address","name":"outputToken","type":"address"},{"indexed":False,"internalType":"int256","name":"slippage","type":"int256"},{"indexed":False,"internalType":"uint32","name":"referralCode","type":"uint32"}],"name":"Swap","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"sender","type":"address"},{"indexed":False,"internalType":"uint256[]","name":"amountsIn","type":"uint256[]"},{"indexed":False,"internalType":"address[]","name":"tokensIn","type":"address[]"},{"indexed":False,"internalType":"uint256[]","name":"amountsOut","type":"uint256[]"},{"indexed":False,"internalType":"address[]","name":"tokensOut","type":"address[]"},{"indexed":False,"internalType":"uint32","name":"referralCode","type":"uint32"}],"name":"SwapMulti","type":"event"},{"inputs":[],"name":"FEE_DENOM","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REFERRAL_WITH_FEE_THRESHOLD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"addressList","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"","type":"uint32"}],"name":"referralLookup","outputs":[{"internalType":"uint64","name":"referralFee","type":"uint64"},{"internalType":"address","name":"beneficiary","type":"address"},{"internalType":"bool","name":"registered","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"_referralCode","type":"uint32"},{"internalType":"uint64","name":"_referralFee","type":"uint64"},{"internalType":"address","name":"_beneficiary","type":"address"}],"name":"registerReferralCode","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_swapMultiFee","type":"uint256"}],"name":"setSwapMultiFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"inputToken","type":"address"},{"internalType":"uint256","name":"inputAmount","type":"uint256"},{"internalType":"address","name":"inputReceiver","type":"address"},{"internalType":"address","name":"outputToken","type":"address"},{"internalType":"uint256","name":"outputQuote","type":"uint256"},{"internalType":"uint256","name":"outputMin","type":"uint256"},{"internalType":"address","name":"outputReceiver","type":"address"}],"internalType":"struct OdosRouterV2.swapTokenInfo","name":"tokenInfo","type":"tuple"},{"internalType":"bytes","name":"pathDefinition","type":"bytes"},{"internalType":"address","name":"executor","type":"address"},{"internalType":"uint32","name":"referralCode","type":"uint32"}],"name":"swap","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"swapCompact","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"internalType":"struct OdosRouterV2.inputTokenInfo[]","name":"inputs","type":"tuple[]"},{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"relativeValue","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"internalType":"struct OdosRouterV2.outputTokenInfo[]","name":"outputs","type":"tuple[]"},{"internalType":"uint256","name":"valueOutMin","type":"uint256"},{"internalType":"bytes","name":"pathDefinition","type":"bytes"},{"internalType":"address","name":"executor","type":"address"},{"internalType":"uint32","name":"referralCode","type":"uint32"}],"name":"swapMulti","outputs":[{"internalType":"uint256[]","name":"amountsOut","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"swapMultiCompact","outputs":[{"internalType":"uint256[]","name":"amountsOut","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"swapMultiFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"contractAddress","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct OdosRouterV2.permit2Info","name":"permit2","type":"tuple"},{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"internalType":"struct OdosRouterV2.inputTokenInfo[]","name":"inputs","type":"tuple[]"},{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"relativeValue","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"internalType":"struct OdosRouterV2.outputTokenInfo[]","name":"outputs","type":"tuple[]"},{"internalType":"uint256","name":"valueOutMin","type":"uint256"},{"internalType":"bytes","name":"pathDefinition","type":"bytes"},{"internalType":"address","name":"executor","type":"address"},{"internalType":"uint32","name":"referralCode","type":"uint32"}],"name":"swapMultiPermit2","outputs":[{"internalType":"uint256[]","name":"amountsOut","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"contractAddress","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct OdosRouterV2.permit2Info","name":"permit2","type":"tuple"},{"components":[{"internalType":"address","name":"inputToken","type":"address"},{"internalType":"uint256","name":"inputAmount","type":"uint256"},{"internalType":"address","name":"inputReceiver","type":"address"},{"internalType":"address","name":"outputToken","type":"address"},{"internalType":"uint256","name":"outputQuote","type":"uint256"},{"internalType":"uint256","name":"outputMin","type":"uint256"},{"internalType":"address","name":"outputReceiver","type":"address"}],"internalType":"struct OdosRouterV2.swapTokenInfo","name":"tokenInfo","type":"tuple"},{"internalType":"bytes","name":"pathDefinition","type":"bytes"},{"internalType":"address","name":"executor","type":"address"},{"internalType":"uint32","name":"referralCode","type":"uint32"}],"name":"swapPermit2","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"internalType":"struct OdosRouterV2.inputTokenInfo[]","name":"inputs","type":"tuple[]"},{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"relativeValue","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"internalType":"struct OdosRouterV2.outputTokenInfo[]","name":"outputs","type":"tuple[]"},{"internalType":"uint256","name":"valueOutMin","type":"uint256"},{"internalType":"bytes","name":"pathDefinition","type":"bytes"},{"internalType":"address","name":"executor","type":"address"}],"name":"swapRouterFunds","outputs":[{"internalType":"uint256[]","name":"amountsOut","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"tokens","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"address","name":"dest","type":"address"}],"name":"transferRouterFunds","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"addresses","type":"address[]"}],"name":"writeAddressList","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]

UNISWAP_V2_ROUTER_ABI = [{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]

UNISWAP_V2_FACTORY_ABI = [{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"token0","type":"address"},{"indexed":True,"internalType":"address","name":"token1","type":"address"},{"indexed":False,"internalType":"address","name":"pair","type":"address"},{"indexed":False,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":True,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"}]