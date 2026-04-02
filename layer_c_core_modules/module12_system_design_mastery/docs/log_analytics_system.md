# Log Analytics System

## Architecture Diagram
```
Agents -> Kafka -> Stream Parse/Enrich -> Object Store (raw)
                               |-> Columnar Index Store
Users -> Query API -> Search Coordinator -> Hot/Warm Nodes
```

## Capacity Estimates
- Ingestion: 15 TB/day raw logs.
- Compression ratio: 6:1.
- Indexed hot retention: 14 days (~35 TB compressed).
- Query SLA: p95 < 2.5s for 95% of queries under 1h window.

## Failure Analysis
- Broker outage: min ISR=3 and rack-aware placement.
- Bad parser release: schema registry compatibility + canary topic.
- Query storms: workload queues with concurrency guards.
- Warm node failures: shard rebalancing with admission controls.

## Cost Analysis
- Stream cluster: ~$160k/month.
- Storage (hot+warm+cold): ~$210k/month.
- Query compute: ~$140k/month.
- Total: ~$510k/month.
