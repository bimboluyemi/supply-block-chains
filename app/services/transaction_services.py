
from ..constants import NODE_ADDRESS, INITIATED, ACTED, RETAILER, SUPPLIER, COURIER

import requests
import json

all_transactions = []
user_trasnsactions = []


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
            if block["block_type"] != '':
                tx = block["transaction"]
                tx["timestamp"] = block["timestamp"]
                tx["node_id"] = block["node_id"]
                tx["block_type"] = block["block_type"]
                content.append(tx)

    global all_transactions
    all_transactions = sorted(content, key=lambda k: k['timestamp'], reverse=True)


def fetch_user_transactions(user):
    """
    get all transactions in the blockchain with the users public key
    :return:
    """
    fetch_transactions()
    d_key = ''
    if len(all_transactions) > 0:
        if user.user_role == RETAILER:
            d_key = 'actor'
        elif user.user_role == SUPPLIER:
            d_key = 'supplier'
        elif user.user_role == COURIER:
            d_key = 'courier'
        else:
            return []
    else:
        return []

    if any(d_key in transaction for transaction in all_transactions):
        user_tx = [tx['node_id'] for tx in all_transactions if tx[d_key] == user.company]
        transaction_ids = set(user_tx)

        return [tx for tx in all_transactions if tx['block_type'] == INITIATED and tx['node_id'] in transaction_ids]
    else:
        return []


def post_transaction(transaction):
    """
    Add an initiated transaction to the blockchain
    :return:
    """
    tx = transaction.__dict__

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(NODE_ADDRESS)

    response = requests.post(new_tx_address, json=tx, headers={'Content-type': 'application/json'})

    if response.status_code == 200:
        return response.content
    else:
        return False


def get_transaction_details(order_number, block_type):
    """
    Get the full details of a transaction
    :param order_number: <str> the node_id of the transaction
    :return:
    """
    fetch_transactions()
    return [tx for tx in all_transactions if tx['block_type'] == block_type and tx['node_id'] == order_number]



