# codes/simulation.py

from .node import Node
import random

NUM_NODES = 10
BYZANTINE_RATIO = 0.3
STEPS = 20
MINING_PROB = 0.5 # chance for each node to mine per step

def run_simulation():
    # Create nodes
    nodes = []
    for i in range(NUM_NODES):
        nodes.append(Node(i, byzantine=(random.random() < BYZANTINE_RATIO)))

    for step in range(1, STEPS + 1):
        print(f"\n--- Step {step} ---")

        # Create a random transaction and broadcast
        sender = random.choice(nodes)
        tx = sender.create_transaction()
        for node in nodes:
            node.receive_transaction(tx)

        # Nodes may mine independently (forks may occur)
        mined_blocks = []
        for node in nodes:
            if random.random() < MINING_PROB:
                block = node.mine_block()
                if block:
                    mined_blocks.append(block)

        # Simulate network propagation delay
        for block in mined_blocks:
            # Broadcast to random subset of nodes first
            subset = random.sample(nodes, k=random.randint(3, NUM_NODES))
            for node in subset:
                node.receive_block(block)

        # Each node processes its pending blocks (longest-chain rule)
        for node in nodes:
            node.process_pending_blocks()

        # Print chain lengths (forks visible if differ)
        chain_lengths = [node.blockchain.length() for node in nodes]
        print(f"Chain lengths: {chain_lengths}")

    # Final chain lengths
    print("\n--- Final chain lengths ---")
    for node in nodes:
        print(f"Node {node.node_id}: {node.blockchain.length()}")

if __name__ == "__main__":
    run_simulation()
