# myproject/settings.py

ETHEREUM_NODE_URL = 'https://<YOUR_ETHEREUM_NODE>'
CONTRACT_ADDRESS = '0x<YOUR_CONTRACT_ADDRESS>'
CONTRACT_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "_name", "type": "string"}
        ],
        "name": "registerPlayer",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_ethAddress", "type": "address"},
            {"name": "_score", "type": "uint256"}
        ],
        "name": "updateScore",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {"name": "_ethAddress", "type": "address"}
        ],
        "name": "getPlayer",
        "outputs": [
            {"name": "", "type": "string"},
            {"name": "", "type": "address"},
            {"name": "", "type": "uint256"}
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]
