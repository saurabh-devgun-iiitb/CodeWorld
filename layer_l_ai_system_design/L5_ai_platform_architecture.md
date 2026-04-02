# Module L5 — AI Platform Architecture

## Topics
- feature store
- orchestration pipelines
- multi-tenant ML systems
- governance

## Artifact: End-to-End ML Platform Design

### Platform Building Blocks
- **Data Plane**: lakehouse, stream ingestion, offline/online feature store.
- **Control Plane**: pipeline orchestration, experiment tracking, model registry.
- **Serving Plane**: model deployment, autoscaling, traffic control.
- **Governance Plane**: lineage, access controls, policy checks, audit logs.

### Multi-tenant Model
- Namespace-based tenant isolation.
- Per-tenant quotas and budget caps.
- Shared control plane with isolated runtime resources.

### Operational Workflows
- Train -> validate -> register -> deploy -> monitor -> retrain.
- Policy gates for PII, drift checks, and responsible-AI guardrails.

### SLOs
- Feature online store availability: 99.99%.
- Model deployment lead time: < 30 minutes for approved models.
- Incident MTTR target: < 30 minutes.
