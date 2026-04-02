# Feature Store

## Architecture Diagram
```
Sources (CDC + Events + Batch) -> Transformation DAGs -> Offline Store
                                                  |-> Online KV Store
Training Pipelines <-> Feature Registry <-> Serving APIs
```

## Capacity Estimates
- 120k feature writes/sec online.
- 9 PB offline historical data.
- 2,500 models consuming shared feature sets.
- Point-in-time join generation target: < 20 min for 1B rows.

## Failure Analysis
- Offline lag spike: backfill DAG priority lanes.
- Online store partition loss: multi-AZ replication + quorum reads.
- Feature drift: automatic checks with rollback to prior feature view.
- Registry corruption: append-only metadata log and signed releases.

## Cost Analysis
- Offline compute + storage: ~$900k/month.
- Online serving store: ~$280k/month.
- Orchestration + governance: ~$120k/month.
- Total: ~$1.3M/month.
