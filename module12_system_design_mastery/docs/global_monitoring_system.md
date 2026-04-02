# Global Monitoring System

## Architecture Diagram
```
Services -> OpenTelemetry Collectors -> Regional Pipelines -> Global Metrics DB
                                          |-> Trace Store
                                          |-> Log Archive
Alert Engine -> Incident Response Bot -> On-call + Status Page
```

## Capacity Estimates
- 25M metrics datapoints/sec globally.
- 3M trace spans/sec sampled.
- 8 TB/day compressed logs.
- Alert fan-out: 30k notifications/hour during incidents.

## Failure Analysis
- Regional telemetry outage: edge buffering + delayed replay.
- Cardinality explosion: dynamic label suppression and quotas.
- Alert fatigue: dedup, grouping, and multi-window burn-rate alerts.
- Control-plane outage: read-only emergency mode + runbook cache.

## Cost Analysis
- Metrics+traces backend: ~$1.8M/month.
- Logging archive/query: ~$600k/month.
- Alerting + incident tooling: ~$150k/month.
- Total: ~$2.55M/month.
