# Module F1 — API & Request Lifecycle

## Topics

- REST vs gRPC tradeoffs
- Request flow: client → load balancer → service → database
- Idempotency keys and retry safety
- Pagination patterns (offset vs cursor)
- Rate limiting (token bucket / leaky bucket)

## Artifact 1: URL Shortener API Design

### API Layer
- `POST /v1/short-urls`
- `GET /v1/{shortCode}`
- `GET /v1/short-urls?cursor=...&limit=...`

### Request Lifecycle
1. Client sends create request with idempotency key.
2. API gateway authenticates + applies rate limit.
3. Service validates URL + generates/allocates code.
4. DB persists mapping with uniqueness constraint.
5. Response returns short code + metadata.

### Idempotency
- Require `Idempotency-Key` header on create.
- Store key hash + response for safe retries.

### Pagination
- Cursor-based listing for user-managed links.

### Rate Limiting
- Per-user write limits and per-IP read limits.

## Artifact 2: Chat Service API Design

### API Layer
- `POST /v1/rooms`
- `POST /v1/rooms/{roomId}/messages`
- `GET /v1/rooms/{roomId}/messages?cursor=...`
- WebSocket: `/v1/ws`

### Request Lifecycle
1. Client opens WebSocket after auth token validation.
2. Message send hits ingress + room shard routing.
3. Service persists message, emits fan-out event.
4. Online users receive push; offline users read on pull.

### Idempotency
- Client message IDs deduplicate retried sends.

### Pagination
- Reverse-chronological cursor retrieval for history.

### Rate Limiting
- Per-room + per-user message rate thresholds.


## Runnable Artifact

- Script: `F1_api_request_lifecycle.py`
- Run: `python3 layer_f_foundation_modules/F1_api_request_lifecycle.py`
