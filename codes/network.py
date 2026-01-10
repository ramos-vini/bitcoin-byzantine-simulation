# codes/network.py

class Network:
    def __init__(self, nodes):
        self.nodes = nodes

    def broadcast_transaction(self, tx):
        for node in self.nodes:
            node.receive_transaction(tx)

    def broadcast_block(self, block):
        for node in self.nodes:
            node.receive_block(block)
