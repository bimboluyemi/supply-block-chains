from .blockchain_services import Blockchain
from uuid import uuid4
from collections import OrderedDict

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200


@app.route('/new_transaction', methods=['POST'])
def add_new_transaction():
    tx_data = request.get_json()

    transaction = validate_request(tx_data)

    if not transaction:
        return 'Invalid Request', 400

    transaction_result = blockchain.submit_transaction(transaction, tx_data['actor'], tx_data['signature'])

    if not transaction_result:
        response = {'message': 'Invalid Transaction!'}
        return jsonify(response), 406
    else:
        # mine a block
        node_id = str(uuid4())[:8].upper()
        block = blockchain.mine('initiated', node_id)
        return jsonify(block), 200


def validate_request(data):

    if not data.get('type'):
        return False
    else:
        type = data['type']
        if type == 'initiated':
            return validate_initiated_request(data)
        elif type == 'acted':
            return validate_acted_request(data)
        elif type == 'tracked':
            return validate_tracked_request(data)
        else:
            return False


def validate_initiated_request(data):
    required = ['actor', 'supplier', 'item', 'quantity', 'signature']
    if not all(k in data for k in required):
        return False

    return OrderedDict({
        'supplier': data['supplier'],
        'item': data['item'],
        'quantity': data['quantity']
    })


def validate_acted_request(data):
    required = ['node_id', 'actor', 'origin', 'destination', 'item', 'quantity', 'action', 'signature']
    if not all(k in data for k in required):
        return False

    return OrderedDict({
        'node_id': data['node_id'],
        'origin': data['origin'],
        'destination': data['destination'],
        'item': data['item'],
        'action': data['action'],
        'quantity': data['quantity']
    })


def validate_tracked_request(data):
    required = ['node_id', 'actor', 'courier', 'status', 'signature']
    if not all(k in data for k in required):
        return False

    return OrderedDict({
        'node_id': data['node_id'],
        'courier': data['courier'],
        'status': data['status']
    })






