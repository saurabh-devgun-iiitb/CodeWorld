# Module F4 — Stateful vs Stateless Systems

## Topics

- Session management patterns
- Token-based authentication
- Sticky sessions tradeoffs
- Distributed state handling

## Artifact: Scalable Session System Design

### Stateless Layer
- Access tokens (JWT or opaque token + introspection) validated at edge/API.
- Services remain stateless for horizontal scaling.

### Stateful Layer
- Refresh token/session records in distributed store (Redis + persistent DB backup).
- Session metadata: device, IP, issued/expiry, revocation status.

### Sticky Sessions
- Avoid by default.
- Use only for legacy websocket affinity edge cases with bounded failover.

### Distributed State
- Global logout through pub/sub invalidation channel.
- Regional replication of session revocation events.
- Grace window for eventual consistency with strict risk controls.

### Reliability Controls
- Token rotation and replay detection.
- Rate-limited refresh endpoints.
- Signed, short-lived access tokens to reduce blast radius.


## Runnable Artifact

- Script: `F4_stateful_vs_stateless.py`
- Run: `python3 layer_f_foundation_modules/F4_stateful_vs_stateless.py`
