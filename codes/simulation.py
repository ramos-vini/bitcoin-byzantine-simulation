# codes/simulation.py

from .node import Node
from .network import Network
import random

NUM_NODES = 10
BYZANTINE_RATIO = 0.3
STEPS = 50

def run_simulation():
    nodes = []
    for i in range(NUM_NODES):
        nodes.append(Node(i, byzantine=(random.random() < BYZANTINE_RATIO)))

    network = Network(nodes)

    for step in range(STEPS):
        sender = random.choice(nodes)
        tx = sender.create_transaction()
        network.broadcast_transaction(tx)

        miner = random.choice(nodes)
        block = miner.mine_block()
        if block:
            network.broadcast_block(block)

    print("Final chain lengths:")
    for node in nodes:
        print(f"Node {node.node_id}: {node.blockchain.length()}")

if __name__ == "__main__":
    run_simulation()
