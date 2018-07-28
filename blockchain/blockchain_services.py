import json
from hashlib import sha256
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import binascii

from Cryptodome.Hash import SHA
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5


MINING_DIFFICULTY = 2


class Blockchain:
    def __init__(self):
        self.transaction = dict()
        self.chain = []
        self.nodes = set()
        # Generate random number to be used as node_id
        self.node_id = str(uuid4()).replace('-', '')
        # Create genesis block
        self.create_block(0, '00', '', '')

    def register_node(self, node_url):
        """
        Add a new node to the list of nodes
        """
        # Checking node_url has valid format
        parsed_url = urlparse(node_url)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    @staticmethod
    def verify_transaction_signature(transaction, actor_key, signature):
        """
        Check that the provided signature corresponds to transaction
        signed by the public key (actor's public key)
        """
        actor_key = actor_key
        public_key = RSA.importKey(binascii.unhexlify(actor_key))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA.new(str(transaction).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(signature))

    def submit_transaction(self, transaction, actor, signature):
        """
        add a transaction to the transaction array if it is verified
        """
        transaction_verified = self.verify_transaction_signature(transaction, actor, signature)
        if transaction_verified:
            self.transaction = transaction
            return len(self.chain) + 1
        else:
            return False

    def create_block(self, nonce, previous_hash, block_type, node_id):
        """
        Add a block to the blockchain
        :return:
        """
        block = {
            'index': len(self.chain) + 1,
            'block_type': block_type,
            'node_id': node_id,
            'transaction': self.transaction,
            'timestamp': time(),
            'nonce': nonce,
            'previous_hash': previous_hash
        }

        # Reset the current transaction
        self.transaction = dict()

        self.chain.append(block)
        return block

    def hash(self, block):
        """
        Create a SHA-256 hash of a block
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()

        return sha256(block_string).hexdigest()

    def proof_of_work(self):
        """
        Proof of work algorithm
        """
        last_block = self.chain[-1]
        last_hash = self.hash(last_block)

        nonce = 0
        while self.valid_proof(self.transaction, last_hash, nonce) is False:
            nonce += 1

        return nonce

    def valid_proof(self, transaction, last_hash, nonce, difficulty=MINING_DIFFICULTY):
        """
        Check if a hash value satisfies the mining conditions. This function is used within the proof_of_work function.
        """
        guess = (str(transaction) + str(last_hash) + str(nonce)).encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[:difficulty] == '0' * difficulty

    def mine(self, block_type, node_id):
        # We run the proof of work algorithm to get the next proof...
        last_block = self.chain[-1]
        nonce = self.proof_of_work()

        # Forge the new Block by adding it to the chain
        previous_hash = self.hash(last_block)
        block = self.create_block(nonce, previous_hash, block_type, node_id)

        return {
            'message': "New Block Forged",
            'block_number': block['index'],
            'transaction': block['transaction'],
            'nonce': block['nonce'],
            'previous_hash': block['previous_hash'],
        }


