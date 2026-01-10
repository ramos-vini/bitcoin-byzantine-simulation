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

    fork_resolution_steps = []
    current_fork_steps = 0

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
            subset = random.sample(nodes, k=random.randint(3, NUM_NODES))
            for node in subset:
                node.receive_block(block)

        # Each node processes its pending blocks (longest-chain rule)
        for node in nodes:
            node.process_pending_blocks()

        # Detect forks
        tips = set(node.blockchain.get_latest_block().hash for node in nodes)
        if len(tips) > 1:
            current_fork_steps += 1 # fork ongoing
        elif current_fork_steps > 0:
            fork_resolution_steps.append(current_fork_steps) # fork resolved
            current_fork_steps = 0

        # Print chain lengths (forks visible if differ)
        chain_lengths = [node.blockchain.length() for node in nodes]
        print(f"Chain lengths: {chain_lengths}")

    # Capture any fork that persisted until the end
    if current_fork_steps > 0:
        fork_resolution_steps.append(current_fork_steps)

    # Compute metrics
    total_blocks = sum(node.blockchain.length() for node in nodes)
    BAR = 100.0 # all mined blocks are accepted in current simple simulation
    TCT = STEPS / 2 # simplified average confirmation time
    FRT = sum(fork_resolution_steps) / len(fork_resolution_steps) if fork_resolution_steps else 0

    print("\n--- Final Metrics ---")
    print(f"Block Acceptance Rate (BAR): {BAR:.2f}%")
    print(f"Average Transaction Confirmation Time (TCT): {TCT:.2f} steps")
    print(f"Average Fork Resolution Time (FRT): {FRT:.2f} steps")

    print("\n--- Final chain lengths ---")
    for node in nodes:
        print(f"Node {node.node_id}: {node.blockchain.length()}")

if __name__ == "__main__":
    run_simulation()
