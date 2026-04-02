# ML Inference Platform

## Architecture Diagram
```
Clients -> API Gateway -> Router -> Model Serving Pool (GPU)
                             |-> Feature Cache
                             |-> Policy + Rate Limits
                             -> Async Logging Bus -> Lakehouse
```

## Capacity Estimates
- Peak traffic: 50k RPS.
- Avg prompt+response tokens: 1,100.
- Effective throughput target: 55M tokens/sec.
- Required GPU replicas (H100 equivalent @ 22k tok/s): ~2,500 with 25% headroom.

## Failure Analysis
- Region loss: active-active failover with DNS + global load balancing.
- Model container crash: pod disruption budgets + warm pool.
- Feature cache outage: graceful degradation to online feature DB.
- Upstream abuse: tenant-aware token buckets with circuit breakers.

## Cost Analysis
- GPU fleet: ~$12.5M/month (blended reserved + spot).
- Network egress: ~$420k/month.
- Control plane + observability: ~$300k/month.
- Total: ~$13.2M/month baseline.
