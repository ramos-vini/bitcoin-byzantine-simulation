# codes/simulation.py

from .node import Node
import random

NUM_NODES = 10
BYZANTINE_RATIO = 0.3
STEPS = 20
MINING_PROB = 0.5 # chance for each node to mine per step

def run_simulation():
    nodes = []
    for i in range(NUM_NODES):
        nodes.append(Node(i, byzantine=(random.random() < BYZANTINE_RATIO)))

    all_blocks_stats = {} # track block acceptance
    tx_confirmation = {} # track transaction confirmation steps
    fork_started_at = None
    FRT_list = []

    tx_id_counter = 0 # unique transaction ids

    for step in range(1, STEPS + 1):
        print(f"\n--- Step {step} ---")

        # Create a random transaction and broadcast
        sender = random.choice(nodes)
        tx = sender.create_transaction()
        tx["id"] = tx_id_counter
        tx_id_counter += 1
        tx_confirmation[tx["id"]] = None # not confirmed yet

        for node in nodes:
            node.receive_transaction(tx)

        # Nodes may mine independently (forks may occur)
        mined_blocks = []
        for node in nodes:
            if random.random() < MINING_PROB:
                block = node.mine_block()
                if block:
                    # Assign block transactions their confirmation step
                    for t in block.transactions:
                        if tx_confirmation[t["id"]] is None:
                            tx_confirmation[t["id"]] = step
                    mined_blocks.append(block)

        # Simulate network propagation delay
        for block in mined_blocks:
            subset = random.sample(nodes, k=random.randint(3, NUM_NODES))
            for node in subset:
                node.receive_block(block)
            all_blocks_stats[block.hash] = {"accepted": False}

        # Each node processes pending blocks
        for node in nodes:
            node.process_pending_blocks()

        # Update block acceptance (BAR)
        for block_hash, stats in all_blocks_stats.items():
            if not stats["accepted"]:
                if any(block_hash == b.hash for n in nodes if not n.byzantine for b in n.blockchain.chain):
                    stats["accepted"] = True

        # Detect forks for FRT
        chain_snapshots = [tuple(node.chain_snapshot()) for node in nodes]
        if len(set(chain_snapshots)) > 1:
            if fork_started_at is None:
                fork_started_at = step
        else:
            if fork_started_at is not None:
                FRT_list.append(step - fork_started_at)
                fork_started_at = None

        # Print chain lengths
        chain_lengths = [node.blockchain.length() for node in nodes]
        print(f"Chain lengths: {chain_lengths}")

    # Final summary
    print("\n--- Final Metrics ---")
    # BAR: fraction of mined blocks by honest nodes that got accepted
    bar = sum(1 for stats in all_blocks_stats.values() if stats["accepted"]) / max(1, len(all_blocks_stats))
    print(f"Block Acceptance Rate (BAR): {bar*100:.2f}%")

    # TCT: average confirmation steps per transaction
    confirmed_tx_steps = [s for s in tx_confirmation.values() if s is not None]
    avg_tct = sum(confirmed_tx_steps)/len(confirmed_tx_steps) if confirmed_tx_steps else 0
    print(f"Average Transaction Confirmation Time (TCT): {avg_tct:.2f} steps")

    # FRT: average fork resolution time
    avg_frt = sum(FRT_list)/len(FRT_list) if FRT_list else 0
    print(f"Average Fork Resolution Time (FRT): {avg_frt:.2f} steps")

    # Print final chain lengths per node
    print("\n--- Final chain lengths ---")
    for node in nodes:
        print(f"Node {node.node_id}: {node.blockchain.length()}")

if __name__ == "__main__":
    run_simulation()
