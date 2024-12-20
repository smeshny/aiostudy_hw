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
        'POL'             : "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        'WPOL'            : "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
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
