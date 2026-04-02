# System Designs Repository (AI + Distributed Computing)

This repository is organized as a learning-focused set of modules.

## Module 1 — Distributed Systems

**Syllabus coverage:**
- Foundations and core distributed systems concepts
- CAP theorem intuition
- Consistency models (strong/eventual mindset)
- Partial failures and fault tolerance
- Logical clocks (conceptual extension point)
- Consensus basics (leader election + replication behavior)

### Python Artifact
`module1_distributed_systems/simulator.py`

A well-commented distributed systems failure simulator that demonstrates:
- Message delays
- Node crashes
- Leader election
- Network partition experiments with observable state divergence

## Quick Start

```bash
python3 module1_distributed_systems/simulator.py
```

The default run includes:
1. Initial leader election
2. Replication under normal conditions
3. A network partition
4. Writes in one partition only
5. Divergence observation
6. Partition healing and final state output
