# System Designs Repository (AI + Distributed Computing)

This repository is organized as a learning-focused set of modules.

## Module 1 — Distributed Systems
- Artifact: `module1_distributed_systems/simulator.py`

## Module 2 — Concurrency & Distributed Transactions
- Artifacts:
  - `module2_concurrency_transactions/design_doc.md`
  - `module2_concurrency_transactions/idempotent_service.py`

## Module 3 — Distributed Storage Systems
- Artifact: `module3_distributed_storage/kv_store.py`

## Module 4 — Messaging & Streaming Systems
- Artifacts:
  - `module4_messaging_streaming/design.md`
  - `module4_messaging_streaming/pipeline_simulation.py`

## Module 5 — Networking & Security
- Artifacts:
  - `module5_networking_security/secure_microservice_platform.md`
  - `module5_networking_security/security_simulation.py`

## Module 6 — Cloud Infrastructure & Kubernetes
- Artifact: `module6_cloud_kubernetes/mini_platform.py`

## Module 7 — Platform Engineering
**Concepts**: developer platforms, CI/CD, GitOps, internal APIs.

**Artifact**: `module7_platform_engineering/internal_developer_platform.py`
- Internal developer platform simulation for 200 engineers.
- Includes deployment pipelines, environment provisioning, service templates.

## Module 8 — Reliability Engineering
**Concepts**: SLOs, error budgets, incident response, chaos engineering.

**Artifact**: `module8_reliability_engineering/reliability_plan.py`
- Reliability plan with SLO definitions, monitoring strategy, and failure injection.

## Module 9 — Observability
**Concepts**: metrics vs logs vs traces, telemetry pipelines, anomaly detection.

**Artifact**: `module9_observability/observability_stack.py`
- End-to-end observability simulation (`service -> exporter -> dashboard`) with latency spike analysis.

## Module 10 — Data Processing Systems
**Concepts**: batch vs streaming, DAG schedulers, windowing.

**Artifact**: `module10_data_processing_systems/analytics_pipeline.py`
- Large-scale analytics pipeline design (ingestion, processing, storage).
- Includes throughput and compute cost estimation.

## Module 11 — ML Infrastructure
**Concepts**: distributed training context, feature stores, inference scaling, model lifecycle.

**Artifact**: `module11_ml_infrastructure/ml_inference_platform.py`
- Multi-tenant inference platform design with autoscaling, model versioning, request batching.

## Module 12 — System Design Mastery
**Concepts**: large-scale architecture, tradeoffs, cost modeling.

**Artifacts**:
- Portfolio validator: `module12_system_design_mastery/portfolio_checker.py`
- Design docs:
  - `module12_system_design_mastery/docs/ml_inference_platform.md`
  - `module12_system_design_mastery/docs/log_analytics_system.md`
  - `module12_system_design_mastery/docs/feature_store.md`
  - `module12_system_design_mastery/docs/global_monitoring_system.md`

Each document includes architecture diagrams, capacity estimates, failure analysis, and cost analysis.

## Quick Start

```bash
python3 module1_distributed_systems/simulator.py
python3 module2_concurrency_transactions/idempotent_service.py
python3 module3_distributed_storage/kv_store.py
python3 module4_messaging_streaming/pipeline_simulation.py
python3 module5_networking_security/security_simulation.py
python3 module6_cloud_kubernetes/mini_platform.py
python3 module7_platform_engineering/internal_developer_platform.py
python3 module8_reliability_engineering/reliability_plan.py
python3 module9_observability/observability_stack.py
python3 module10_data_processing_systems/analytics_pipeline.py
python3 module11_ml_infrastructure/ml_inference_platform.py
python3 module12_system_design_mastery/portfolio_checker.py
```
