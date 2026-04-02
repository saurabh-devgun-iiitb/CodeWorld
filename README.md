# System Designs Repository (AI + Distributed Computing)

This repository is organized as a learning-focused set of modules.

## Module 1 — Distributed Systems
- Artifact: `layer_c_core_modules/module1_distributed_systems/simulator.py`

## Module 2 — Concurrency & Distributed Transactions
- Artifacts:
  - `layer_c_core_modules/module2_concurrency_transactions/design_doc.md`
  - `layer_c_core_modules/module2_concurrency_transactions/idempotent_service.py`

## Module 3 — Distributed Storage Systems
- Artifact: `layer_c_core_modules/module3_distributed_storage/kv_store.py`

## Module 4 — Messaging & Streaming Systems
- Artifacts:
  - `layer_c_core_modules/module4_messaging_streaming/design.md`
  - `layer_c_core_modules/module4_messaging_streaming/pipeline_simulation.py`

## Module 5 — Networking & Security
- Artifacts:
  - `layer_c_core_modules/module5_networking_security/secure_microservice_platform.md`
  - `layer_c_core_modules/module5_networking_security/security_simulation.py`

## Module 6 — Cloud Infrastructure & Kubernetes
- Artifact: `layer_c_core_modules/module6_cloud_kubernetes/mini_platform.py`

## Module 7 — Platform Engineering
**Concepts**: developer platforms, CI/CD, GitOps, internal APIs.

**Artifact**: `layer_c_core_modules/module7_platform_engineering/internal_developer_platform.py`
- Internal developer platform simulation for 200 engineers.
- Includes deployment pipelines, environment provisioning, service templates.

## Module 8 — Reliability Engineering
**Concepts**: SLOs, error budgets, incident response, chaos engineering.

**Artifact**: `layer_c_core_modules/module8_reliability_engineering/reliability_plan.py`
- Reliability plan with SLO definitions, monitoring strategy, and failure injection.

## Module 9 — Observability
**Concepts**: metrics vs logs vs traces, telemetry pipelines, anomaly detection.

**Artifact**: `layer_c_core_modules/module9_observability/observability_stack.py`
- End-to-end observability simulation (`service -> exporter -> dashboard`) with latency spike analysis.

## Module 10 — Data Processing Systems
**Concepts**: batch vs streaming, DAG schedulers, windowing.

**Artifact**: `layer_c_core_modules/module10_data_processing_systems/analytics_pipeline.py`
- Large-scale analytics pipeline design (ingestion, processing, storage).
- Includes throughput and compute cost estimation.

## Module 11 — ML Infrastructure
**Concepts**: distributed training context, feature stores, inference scaling, model lifecycle.

**Artifact**: `layer_c_core_modules/module11_ml_infrastructure/ml_inference_platform.py`
- Multi-tenant inference platform design with autoscaling, model versioning, request batching.

## Module 12 — System Design Mastery
**Concepts**: large-scale architecture, tradeoffs, cost modeling.

**Artifacts**:
- Portfolio validator: `layer_c_core_modules/module12_system_design_mastery/portfolio_checker.py`
- Design docs:
  - `layer_c_core_modules/module12_system_design_mastery/docs/ml_inference_platform.md`
  - `layer_c_core_modules/module12_system_design_mastery/docs/log_analytics_system.md`
  - `layer_c_core_modules/module12_system_design_mastery/docs/feature_store.md`
  - `layer_c_core_modules/module12_system_design_mastery/docs/global_monitoring_system.md`

Each document includes architecture diagrams, capacity estimates, failure analysis, and cost analysis.

## Quick Start

```bash
python3 layer_c_core_modules/module1_distributed_systems/simulator.py
python3 layer_c_core_modules/module2_concurrency_transactions/idempotent_service.py
python3 layer_c_core_modules/module3_distributed_storage/kv_store.py
python3 layer_c_core_modules/module4_messaging_streaming/pipeline_simulation.py
python3 layer_c_core_modules/module5_networking_security/security_simulation.py
python3 layer_c_core_modules/module6_cloud_kubernetes/mini_platform.py
python3 layer_c_core_modules/module7_platform_engineering/internal_developer_platform.py
python3 layer_c_core_modules/module8_reliability_engineering/reliability_plan.py
python3 layer_c_core_modules/module9_observability/observability_stack.py
python3 layer_c_core_modules/module10_data_processing_systems/analytics_pipeline.py
python3 layer_c_core_modules/module11_ml_infrastructure/ml_inference_platform.py
python3 layer_c_core_modules/module12_system_design_mastery/portfolio_checker.py
```

## Layer C — Core 12 Modules (Enhanced Execution)

The existing 12-module structure remains unchanged, but each module artifact should now explicitly include the following cross-cutting dimensions:

1. API layer
2. Data model
3. Caching strategy
4. Cost modeling (traffic/QPS, data volume, infra required, cost per request)
5. Security (authn/authz, secret management, tenant isolation, data access control)
6. Performance engineering (p50/p99 latency, throughput, bottlenecks)
7. Failure modes
8. Evolution strategy
9. Product thinking (user, critical vs optional, graceful degradation)

Reference template: `layer_c_core_modules/enhancement_requirements.md`

## Layer F — Foundation Modules

A new foundational layer is now available at:

- `layer_f_foundation_modules/README.md`
- `layer_c_core_modules/README.md`

It includes modules F1–F5 covering APIs, storage modeling, caching, state management, and system migration.

## Layer L — AI System Design (Leverage Layer)

A focused add-on layer for AI system design is available at:

- `layer_l_ai_system_design/README.md`

It includes modules L1–L5 for ML architecture, serving systems, distributed training, retrieval/vector search, and end-to-end AI platform design.
