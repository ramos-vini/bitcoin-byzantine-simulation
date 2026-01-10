# codes/blockchain.py

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        from .block import Block
        return Block("0", [])

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, block):
        if block.valid and block.prev_hash == self.get_latest_block().hash:
            self.chain.append(block)
            return True  # block accepted
        return False  # block rejected

    def length(self):
        return len(self.chain)
