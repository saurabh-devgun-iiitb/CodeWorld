# Module F3 — Caching & Performance Layer

## Topics

- CDN edge caching
- Redis caching patterns
- Cache invalidation strategies
- Read/write optimization

## Artifact: Add Caching Layer to News Feed / Timeline

### Baseline Flow
- Feed read service fetches ranked posts from DB + graph store.

### Caching Layer
- **CDN**: cache media + static profile assets.
- **Redis**:
  - timeline page cache per user (`timeline:{userId}:{cursor}`)
  - object cache for post metadata (`post:{postId}`)
  - relationship cache for follower graph hot keys

### Invalidation
- Write-through for post creates.
- Event-driven invalidation on edits/deletes.
- Time-based TTL fallback to prevent stale lock-in.

### Read/Write Optimization
- Fan-out-on-write for highly active users.
- Fan-out-on-read for long-tail users.
- Precompute top-N timeline window for hot sessions.

### Performance Targets Example
- p99 timeline read latency < 250 ms.
- Cache hit ratio > 85% for hot cohorts.


## Runnable Artifact

- Script: `F3_caching_performance.py`
- Run: `python3 layer_f_foundation_modules/F3_caching_performance.py`
