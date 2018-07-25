
from ..constants import NODE_ADDRESS

import requests
import json

all_transactions = []


def fetch_transactions():
    """
    Fetch the blockchain data and store it locally
    """

    get_chain_address = "{}/chain".format(NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            tx = block["transaction"]
            tx["timestamp"] = block["timestamp"]
            tx["node_id"] = block["node_id"]
            tx["block_type"] = block["block_type"]
            content.append(tx)

    global all_transactions
    all_transactions = sorted(content, key=lambda k: k['timestamp'], reverse=True)


def fetch_user_transactions(user_public_key):
    """
    get all transactions in the blockchain with the users public key
    :return:
    """
    fetch_transactions()
    user_tx = [tx for tx in all_transactions if tx["actor"] == user_public_key or tx['supplier'] == user_public_key
               or tx['courier'] == user_public_key]

    return user_tx


def post_transaction(transaction):
    """
    Add an initiated transaction to the blockchain
    :return:
    """
    tx = json.dumps(transaction)

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(NODE_ADDRESS)

    response = requests.post(new_tx_address, json=tx, headers={'Content-type': 'application/json'})

    if response.status_code == 200:
        return response.content
    else:
        return False





