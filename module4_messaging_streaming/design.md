# Event-Driven Analytics Pipeline (Design)

## Architecture

producer → message log → stream processor → storage

- **Producer**: emits click/order events with event IDs.
- **Message Log**: append-only partitions, offset-based consumption.
- **Consumer Group**: multiple processors sharing partitions.
- **Stream Processor**: parses events, computes aggregates, writes sink updates.
- **Storage**: analytics sink (e.g., OLAP table / timeseries DB).

## Exactly-Once Semantics (practical)

- Producer uses deterministic event IDs.
- Processor tracks committed offsets + idempotent sink upserts.
- On restart, processor replays from last committed offset; duplicate outputs suppressed by event ID.

## Backpressure

- Monitor lag = `log_end_offset - committed_offset`.
- If lag exceeds threshold:
  - slow producer
  - increase consumer concurrency
  - batch processing size adjustment

## Experiment Plan

1. Generate bursty traffic (high throughput).
2. Introduce artificial consumer slowdown.
3. Observe lag and recovery time under autoscale of workers.
