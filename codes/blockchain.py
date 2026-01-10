# codes/blockchain.py

from .block import Block

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("0", [])

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, block):
        if block.prev_hash == self.get_latest_block().hash:
            self.chain.append(block)
            return True
        return False

    def length(self):
        return len(self.chain)

    # Replace local chain if new_chain is longer and valid
    def replace_chain(self, new_chain):
        if len(new_chain) > len(self.chain) and self.is_valid_chain(new_chain):
            self.chain = new_chain.copy()
            return True
        return False

    # Validate if each block's prev_hash matches the previous block
    def is_valid_chain(self, chain):
        for i in range(1, len(chain)):
            if chain[i].prev_hash != chain[i-1].hash:
                return False
        return True
