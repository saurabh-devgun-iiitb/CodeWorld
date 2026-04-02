# Module L3 — Distributed Training Systems

## Topics
- data parallelism
- model parallelism
- gradient sync (all-reduce)
- GPU utilization

## Artifact: Distributed Training Pipeline Design

### Architecture
1. Dataset sharding and preprocessing on distributed storage.
2. Training orchestrator schedules jobs on GPU cluster.
3. Workers run mixed precision training.
4. Parameter/gradient sync through all-reduce.
5. Checkpointing + validation + model registry publish.

### Parallelism Strategy
- Data parallel for moderate models.
- Tensor/model parallel + pipeline parallel for very large models.

### Reliability Controls
- Periodic checkpoints (every N steps).
- Elastic training to tolerate worker preemption.
- Resume-from-checkpoint recovery.

### Efficiency Targets
- GPU utilization > 70% sustained.
- End-to-end training throughput measured in samples/sec.
- Straggler mitigation via balanced sharding + adaptive batch sizing.
