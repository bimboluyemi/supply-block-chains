from .blockchain_services import Blockchain
from .constants import INITIATED
from .request_validations import validate_request
from uuid import uuid4

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

    transaction_result = blockchain.submit_transaction(transaction, tx_data['actor_key'], tx_data['signature'])

    if not transaction_result:
        response = {'message': 'Invalid Transaction!'}
        return jsonify(response), 406
    else:
        # mine a block
        block_type = tx_data['block_type']
        node_id = str(uuid4())[:8].upper() if block_type == INITIATED else tx_data['node_id']
        block = blockchain.mine(block_type, node_id)
        return jsonify(block), 200







