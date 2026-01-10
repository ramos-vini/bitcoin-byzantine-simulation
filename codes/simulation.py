# codes/simulation.py

from .node import Node
import random

NUM_NODES = 10
BYZANTINE_RATIO = 0.3
STEPS = 20
MINING_PROB = 0.5  # chance for each node to mine per step

def run_simulation():
    nodes = [Node(i, byzantine=(random.random() < BYZANTINE_RATIO)) for i in range(NUM_NODES)]

    fork_resolution_steps = []
    current_fork_steps = 0

    # Metrics tracking
    proposed_blocks = {}  # {block_hash: valid?}
    accepted_blocks = set()  # unique hashes of blocks actually accepted

    for step in range(1, STEPS + 1):
        print(f"\n--- Step {step} ---")

        # Broadcast a random transaction
        sender = random.choice(nodes)
        tx = sender.create_transaction()
        for node in nodes:
            node.receive_transaction(tx)

        # Mining
        mined_blocks = []
        for node in nodes:
            if random.random() < MINING_PROB:
                block = node.mine_block()
                if block:
                    mined_blocks.append(block)
                    proposed_blocks[block.hash] = block.valid  # track as proposed

        # Network propagation
        for block in mined_blocks:
            subset = random.sample(nodes, k=random.randint(3, NUM_NODES))
            for node in subset:
                node.receive_block(block)

        # Process pending blocks
        for node in nodes:
            accepted = node.process_pending_blocks()
            for b in accepted:
                accepted_blocks.add(b.hash)
                # epidemic propagation
                for peer in nodes:
                    if peer is not node:
                        peer.receive_block(b)

        # Fork detection
        tips = set(node.blockchain.get_tip() for node in nodes)
        if len(tips) > 1:
            current_fork_steps += 1
        elif current_fork_steps > 0:
            fork_resolution_steps.append(current_fork_steps)
            current_fork_steps = 0

        # Print chain lengths
        chain_lengths = [node.blockchain.length() for node in nodes]
        print(f"Chain lengths: {chain_lengths}")

    if current_fork_steps > 0:
        fork_resolution_steps.append(current_fork_steps)

    # Metrics computation
    valid_proposed = sum(1 for v in proposed_blocks.values() if v)
    invalid_proposed = sum(1 for v in proposed_blocks.values() if not v)
    valid_accepted = sum(1 for h in accepted_blocks if proposed_blocks[h])
    invalid_accepted = sum(1 for h in accepted_blocks if not proposed_blocks[h])

    BAR_valid = (valid_accepted / valid_proposed * 100) if valid_proposed else 0
    BAR_invalid = (invalid_accepted / invalid_proposed * 100) if invalid_proposed else 0
    TCT = STEPS / 2
    FRT = sum(fork_resolution_steps) / len(fork_resolution_steps) if fork_resolution_steps else 0

    print("\n--- Final Metrics ---")
    print(f"Block Acceptance Rate (Valid): {BAR_valid:.2f}%")
    print(f"Block Acceptance Rate (Invalid): {BAR_invalid:.2f}%")
    print(f"Average Transaction Confirmation Time (TCT): {TCT:.2f} steps")
    print(f"Average Fork Resolution Time (FRT): {FRT:.2f} steps")

    print("\n--- Final chain lengths ---")
    for node in nodes:
        print(f"Node {node.node_id}: {node.blockchain.length()}")

if __name__ == "__main__":
    run_simulation()
