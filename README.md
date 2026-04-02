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

---

## Module 2 — Concurrency & Distributed Transactions

### Concepts
- idempotency
- two-phase commit
- saga pattern
- optimistic vs pessimistic locking

### Artifacts
- Design doc: `module2_concurrency_transactions/design_doc.md`
- Executable prototype: `module2_concurrency_transactions/idempotent_service.py`

Outcome: Understand correctness guarantees in distributed payment workflows.

---

## Module 3 — Distributed Storage Systems

### Concepts
- LSM trees (conceptual)
- partitioning
- replication
- quorum reads/writes

### Artifact
- Executable prototype: `module3_distributed_storage/kv_store.py`

Features:
- consistent hashing
- replication
- quorum reads

Outcome: Build intuition for Dynamo-style storage systems.

---

## Module 4 — Messaging & Streaming Systems

### Concepts
- event logs
- consumer groups
- exactly-once semantics (practical)
- backpressure

### Artifacts
- Design doc: `module4_messaging_streaming/design.md`
- Executable prototype: `module4_messaging_streaming/pipeline_simulation.py`

Outcome: Understand throughput, lag, and recovery in stream processing.

---

## Module 5 — Networking & Security

### Concepts
- service mesh
- mTLS
- network partitions
- secret management

### Artifacts
- Architecture doc: `module5_networking_security/secure_microservice_platform.md`
- Executable prototype: `module5_networking_security/security_simulation.py`

Outcome: Reason about secure service-to-service communication and policy.

---

## Module 6 — Cloud Infrastructure & Kubernetes

### Concepts
- scheduling
- container lifecycle
- resource isolation
- autoscaling

### Artifact
- Executable prototype: `module6_cloud_kubernetes/mini_platform.py`

Outcome: Build operational intuition for cluster platform behavior.

## Quick Start

```bash
python3 module1_distributed_systems/simulator.py
python3 module2_concurrency_transactions/idempotent_service.py
python3 module3_distributed_storage/kv_store.py
python3 module4_messaging_streaming/pipeline_simulation.py
python3 module5_networking_security/security_simulation.py
python3 module6_cloud_kubernetes/mini_platform.py
```
