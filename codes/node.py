# codes/node.py

import random
from .blockchain import Blockchain
from .block import Block

class Node:
    def __init__(self, node_id, byzantine=False):
        self.node_id = node_id
        self.byzantine = byzantine
        genesis = Block("0", [])
        genesis.mine()
        self.blockchain = Blockchain(genesis)
        self.transactions = []  # mempool
        self.pending_blocks = []  # blocks received but not yet processed

    def create_transaction(self, step):
        tx = {
            "sender": self.node_id,
            "receiver": random.randint(0, 9),
            "amount": random.randint(1, 100),
            "step_created": step  # track creation step
        }
        if self.byzantine and random.random() < 0.5:
            tx["amount"] = -tx["amount"]
        self.transactions.append(tx)
        return tx

    def receive_transaction(self, tx):
        if self.byzantine and random.random() < 0.2:
            return  # ignore some tx
        self.transactions.append(tx)

    # Mine a block from local tip; returns block or None
    def mine_block(self):
        if not self.transactions:
            return None
        prev_hash = self.blockchain.get_tip()
        block = Block(prev_hash, self.transactions.copy())
        block.mine()  # simplified PoW

        # Byzantine nodes may produce invalid blocks
        block.valid = True
        if self.byzantine and random.random() < 0.3:  # 30% chance block is invalid
            block.valid = False

        self.transactions = []  # clear mempool
        return block

    # Store block in pending queue to simulate network delay
    def receive_block(self, block):
        if block:
            self.pending_blocks.append(block)

    # Resolve pending blocks using longest-chain rule
    # Returns accepted blocks AND confirmed transactions for TCT
    def process_pending_blocks(self, step):
        accepted_blocks = []
        confirmed_transactions = []

        for block in self.pending_blocks:
            if self.blockchain.add_block(block):
                accepted_blocks.append(block)
                for tx in block.transactions:
                    tx["step_confirmed"] = step
                    confirmed_transactions.append(tx)

        self.pending_blocks = []
        return accepted_blocks, confirmed_transactions

    # Optional: show snapshot of main chain
    def chain_snapshot(self):
        snapshot = []
        for b_hash in self.blockchain.blocks:
            block = self.blockchain.blocks[b_hash]
            if block and block.hash:
                snapshot.append(block.hash[:6])
            else:
                snapshot.append("------")
        return snapshot
