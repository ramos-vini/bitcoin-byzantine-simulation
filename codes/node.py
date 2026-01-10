# codes/node.py

from .blockchain import Blockchain
from .block import Block
from .transaction import Transaction
import random

class Node:
    def __init__(self, node_id, byzantine=False):
        self.node_id = node_id
        self.byzantine = byzantine
        self.blockchain = Blockchain()
        self.mempool = []

    def create_transaction(self):
        if self.byzantine and random.random() < 0.5:
            # Invalid transaction (negative amount)
            return Transaction(self.node_id, "X", -100)
        return Transaction(self.node_id, random.randint(0, 10), random.randint(1, 10))

    def receive_transaction(self, tx):
        if tx.amount > 0:
            self.mempool.append(tx)

    def mine_block(self):
        if not self.mempool:
            return None

        block = Block(
            self.blockchain.get_latest_block().hash,
            self.mempool[:2]
        )
        block.mine()
        self.mempool = []
        return block

    # Add block if it extends the chain, or replace chain if needed
    def receive_block(self, block):
        added = self.blockchain.add_block(block)
        if not added:
            simulated_new_chain = self.blockchain.chain + [block]
            self.blockchain.replace_chain(simulated_new_chain)
