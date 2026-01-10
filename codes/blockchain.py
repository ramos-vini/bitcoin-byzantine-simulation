# codes/blockchain.py

class Blockchain:
    def __init__(self, genesis_block):
        # block_hash -> Block
        self.blocks = {genesis_block.hash: genesis_block}

        # block_hash -> height
        self.heights = {genesis_block.hash: 0}

        # hash of the current best chain tip
        self.tip = genesis_block.hash

    def add_block(self, block):
        # Reject invalid blocks
        if not block.valid:
            return False

        # Parent must exist
        if block.prev_hash not in self.blocks:
            return False

        parent_height = self.heights[block.prev_hash]
        block_height = parent_height + 1

        self.blocks[block.hash] = block
        self.heights[block.hash] = block_height

        # Longest-chain rule
        if block_height > self.heights[self.tip]:
            self.tip = block.hash

        return True

    def length(self):
        # height starts at 0 for genesis
        return self.heights[self.tip] + 1

    def get_tip(self):
        return self.tip
