# codes/block.py

class Block:
    def __init__(self, prev_hash, transactions):
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.nonce = 0
        self.hash = None

    def mine(self, difficulty=1000):
        while True:
            if self.nonce % difficulty == 0:
                self.hash = f"{self.prev_hash}-{self.nonce}"
                break
            self.nonce += 1
