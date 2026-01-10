# codes/block.py

import hashlib
import random

class Block:
    def __init__(self, prev_hash, transactions):
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.nonce = 0
        self.hash = None
        self.valid = all(tx.get("amount", 0) > 0 for tx in transactions)  # simple validity check

    def compute_hash(self):
        data = str(self.prev_hash) + str(self.transactions) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

    def mine(self, difficulty=2):
        prefix = '0' * difficulty
        while True:
            self.hash = self.compute_hash()
            if self.hash.startswith(prefix):
                break
            self.nonce += 1
        if self.hash is None:
            self.hash = self.compute_hash()

