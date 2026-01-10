# Bitcoin-Inspired Byzantine Node Simulation

This is a simplified Python simulation of a Bitcoin-inspired blockchain network designed for academic purposes, specifically to demonstrate decentralized consensus, fork resolution, and transaction confirmation under Byzantine conditions.

---

## Overview

The simulation consists of:

- **Nodes**: Each node maintains its own blockchain and mempool of transactions. Some nodes can behave Byzantine (maliciously), producing invalid transactions or blocks.
- **Blocks**: Contain transactions, a reference to the previous block hash, and a simple Proof-of-Work.
- **Blockchain**: Each node follows the longest-chain rule to maintain consensus.
- **Transactions**: Randomly generated between nodes; invalid transactions are rejected by honest nodes.

The system tracks key evaluation metrics:

1. **Block Acceptance Rate (BAR)**: Percentage of valid and invalid blocks accepted by the network.
2. **Transaction Confirmation Time (TCT)**: Average number of steps it takes for a transaction to be included in the main chain.
3. **Fork Resolution Time (FRT)**: Average number of steps to resolve competing chains and reach consensus.

---

## Key Features

- Decentralized consensus using the **longest-chain rule**.
- Handling of **Byzantine nodes**, simulating network faults and malicious behavior.
- Realistic measurement of **transaction confirmation time (TCT)** and **fork resolution time (FRT)**.
- Simple, minimalistic design to clearly illustrate blockchain dynamics.
- Metrics printed after each simulation run for easy analysis.

---

## Getting Started

### Requirements

- Python 3.8+
- Standard libraries (`hashlib`, `random`)

### Running the Simulation

```bash
git clone <repository_url>
cd bitcoin-byzantine-simulation
python3 -m codes.simulation
