# codes/simulation.py

from .node import Node
import random
from collections import Counter

NUM_NODES = 1000
BYZANTINE_RATIO = 0.3
STEPS = 100
MINING_PROB = 0.5  # chance for each node to mine per step

def run_simulation():
    nodes = [Node(i, byzantine=(random.random() < BYZANTINE_RATIO)) for i in range(NUM_NODES)]

    fork_resolution_steps = []
    fork_active = False
    fork_start_step = None

    proposed_blocks = {}  # {block_hash: valid?}
    accepted_blocks = set()  # unique hashes of blocks actually accepted
    all_confirmed_txs = []  # track confirmed transactions for TCT

    for step in range(1, STEPS + 1):
        print(f"\n--- Step {step} ---")

        # Broadcast a random transaction
        sender = random.choice(nodes)
        tx = sender.create_transaction(step)
        for node in nodes:
            node.receive_transaction(tx)

        # Mining
        mined_blocks = []
        for node in nodes:
            if random.random() < MINING_PROB:
                block = node.mine_block()
                if block:
                    mined_blocks.append(block)
                    proposed_blocks[block.hash] = block.valid

        # Network propagation
        for block in mined_blocks:
            subset = random.sample(nodes, k=random.randint(3, NUM_NODES))
            for node in subset:
                node.receive_block(block)

        # Process pending blocks
        for node in nodes:
            accepted, confirmed_txs = node.process_pending_blocks(step)
            for b in accepted:
                accepted_blocks.add(b.hash)
            all_confirmed_txs.extend(confirmed_txs)

        # ----------------------------
        # Fork detection & resolution
        # (>50% consensus definition)
        # ----------------------------
        tips = [node.blockchain.get_tip() for node in nodes]
        tip_counts = Counter(tips)

        dominant_share = max(tip_counts.values()) / NUM_NODES

        # Fork starts
        if len(tip_counts) > 1 and not fork_active:
            fork_active = True
            fork_start_step = step

        # Fork resolves when >50% agree
        if fork_active and dominant_share > 0.5:
            fork_resolution_steps.append(step - fork_start_step)
            fork_active = False
            fork_start_step = None

        chain_lengths = [node.blockchain.heights[node.blockchain.get_tip()] + 1 for node in nodes]
        print(f"Chain lengths: {chain_lengths}")

    # Close unresolved fork (if any)
    if fork_active:
        fork_resolution_steps.append(STEPS - fork_start_step)

    # Metrics computation
    valid_proposed = sum(1 for v in proposed_blocks.values() if v)
    invalid_proposed = sum(1 for v in proposed_blocks.values() if not v)
    valid_accepted = sum(1 for h in accepted_blocks if proposed_blocks[h])
    invalid_accepted = sum(1 for h in accepted_blocks if not proposed_blocks[h])

    BAR_valid = (valid_accepted / valid_proposed * 100) if valid_proposed else 0
    BAR_invalid = (invalid_accepted / invalid_proposed * 100) if invalid_proposed else 0

    tct_list = [
        tx["step_confirmed"] - tx["step_created"]
        for tx in all_confirmed_txs
        if "step_created" in tx and "step_confirmed" in tx
    ]
    TCT = sum(tct_list) / len(tct_list) if tct_list else 0

    FRT = sum(fork_resolution_steps) / len(fork_resolution_steps) if fork_resolution_steps else 0

    print("\n--- Final Metrics ---")
    print(f"Block Acceptance Rate (Valid): {BAR_valid:.2f}%")
    print(f"Block Acceptance Rate (Invalid): {BAR_invalid:.2f}%")
    print(f"Average Transaction Confirmation Time (TCT): {TCT:.2f} steps")
    print(f"Average Fork Resolution Time (FRT): {FRT:.2f} steps")

    print("\n--- Final chain lengths ---")
    for node in nodes:
        print(f"Node {node.node_id}: {node.blockchain.heights[node.blockchain.get_tip()] + 1}")

if __name__ == "__main__":
    run_simulation()
