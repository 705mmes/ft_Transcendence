# myapp/utils.py
from web3 import Web3
from django.conf import settings
import secrets

w3 = Web3(Web3.HTTPProvider(settings.ETHEREUM_NODE_URL))
contract = w3.eth.contract(address=settings.CONTRACT_ADDRESS, abi=settings.CONTRACT_ABI)

def generate_wallet():
    private_key = '0x' + secrets.token_hex(32)
    account = w3.eth.account.privateKeyToAccount(private_key)
    return account.address, private_key

def register_player_on_blockchain(name, private_key):
    account = w3.eth.account.privateKeyToAccount(private_key)
    tx = contract.functions.registerPlayer(name).buildTransaction({
        'chainId': 1,  # Replace with the appropriate chain ID
        'gas': 70000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': w3.eth.getTransactionCount(account.address),
    })

    signed_tx = w3.eth.account.signTransaction(tx, private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash.hex()

def update_score_on_blockchain(eth_address, score, private_key):
    account = w3.eth.account.privateKeyToAccount(private_key)
    tx = contract.functions.updateScore(eth_address, score).buildTransaction({
        'chainId': 1,
        'gas': 70000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': w3.eth.getTransactionCount(account.address),
    })

    signed_tx = w3.eth.account.signTransaction(tx, private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash.hex()
