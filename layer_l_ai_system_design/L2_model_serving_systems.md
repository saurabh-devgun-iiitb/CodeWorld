# Module L2 — Model Serving Systems

## Topics
- batching
- latency optimization
- model versioning
- A/B testing

## Artifact: Real-time Inference API Design

### Serving Architecture
- API Gateway -> Inference Router -> Model Servers -> Feature Store/Cache
- Dynamic micro-batching window (e.g., 5–20 ms) for GPU efficiency.

### API Contracts
- `POST /v1/inference/{modelName}` with `{inputs, context, model_version?}`
- `GET /v1/models/{modelName}/versions`

### Versioning + Experimentation
- Shadow deploy new model versions before traffic shift.
- A/B split (e.g., 90/10), then progressive rollout based on KPIs.
- Automatic rollback on error-rate or p99-latency violations.

### Latency Optimization
- Warm model pools.
- Feature cache for hot entities.
- Request coalescing + async logging.

### Targets
- p99 latency < 120 ms for online inference.
- Availability target: 99.95%.
