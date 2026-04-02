# Transaction Strategy for a Distributed Payment System

## 1) Architecture

**Core services**
- **API Gateway**: Auth, rate limits, request ID propagation.
- **Payment Orchestrator**: Runs saga workflow and state machine.
- **Ledger Service**: Immutable double-entry accounting records.
- **Wallet Service**: Balance reservation/debit/credit operations.
- **Risk/Fraud Service**: Asynchronous risk scoring and hold decisions.
- **Notification Service**: User-facing status updates.
- **Outbox + Event Bus**: Reliable event publishing from local transactions.

**Data flow (happy path)**
1. Client sends `POST /payments` with an idempotency key.
2. Orchestrator creates payment intent (`PENDING`).
3. Wallet reserves funds (or capture from external provider).
4. Ledger records entries.
5. Orchestrator marks payment `COMPLETED` and emits domain events.

## 2) Transaction Model

### Idempotency
- Every mutating API requires `Idempotency-Key` scoped by `(tenant_id, route)`.
- Persist request hash + terminal response.
- Replays return the original response; mismatched payload hash returns `409`.

### Two-Phase Commit (2PC)
- **Use narrowly** for tightly-coupled internal resources where global atomicity is required.
- Coordinator: payment orchestrator transaction manager.
- Participants: wallet + ledger.
- Downsides: coordinator blocking under failures, operational complexity.

### Saga Pattern (default)
- Use orchestrated saga for cross-service payment flow.
- Steps:
  1. Create payment intent
  2. Reserve/capture funds
  3. Commit ledger entries
  4. Emit payment-completed event
- Compensation examples:
  - Reserve succeeded, ledger failed → release reservation.
  - External capture succeeded, local ledger failed → issue refund/void.

### Locking Strategy
- **Optimistic locking** (version column / compare-and-swap) for high-contention read-mostly entities.
- **Pessimistic locking** for short critical sections requiring strict serialization.
- Recommended default: optimistic on payment intents + retries; pessimistic for wallet debit rows in final commit path.

## 3) Failure Recovery

- Persist saga state transitions in durable storage.
- Use outbox pattern: local DB transaction writes business state + pending events atomically.
- Background dispatcher publishes outbox events with dedupe keys.
- Crash recovery replays incomplete sagas from last durable step.
- Poison messages go to DLQ with retry metadata and causality IDs.

## 4) Retry Strategy

- Retry only on transient errors (timeouts, 5xx, rate-limit).
- Exponential backoff + jitter (e.g., base 100ms, cap 10s).
- Max attempts per step + circuit breaker on downstream failure spikes.
- All retries must carry original idempotency key.
- For external PSP calls, include provider-side idempotency key too.

## 5) Correctness Guarantees

- **No duplicate charge intent execution** under client retries due to API idempotency.
- **At-least-once event delivery** with idempotent consumers.
- **Eventual consistency** across services, with compensations preserving invariants.
- **Ledger immutability** ensures auditability even during rollback-like compensations.

## 6) Operational Notes

- Emit tracing spans keyed by `payment_id` and `idempotency_key`.
- SLOs: p95 end-to-end latency, saga completion rate, compensation rate, duplicate suppression hits.
- Chaos tests: network partitions, delayed messages, participant crash during each saga step.
