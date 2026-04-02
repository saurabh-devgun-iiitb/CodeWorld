# Module L1 — ML System Architecture

## Topics
- offline vs online pipelines
- feature engineering
- training vs inference split

## Artifact: Recommendation System Pipeline Design

### High-level Architecture
1. **Offline data pipeline**: ingest clicks, views, purchases into data lake.
2. **Feature engineering jobs**: build user/item/context features daily/hourly.
3. **Training pipeline**: train retrieval + ranking models offline.
4. **Model registry**: store model versions and evaluation metadata.
5. **Online inference pipeline**: fetch fresh features + score candidates.

### Key Design Choices
- Offline-heavy feature generation for cost efficiency.
- Online feature enrichment for freshness (session signals).
- Separate retrieval model (fast, broad) and ranking model (slower, precise).

### Interfaces
- `POST /v1/recommendations:rank` for online ranking.
- `GET /v1/users/{id}/features` for feature retrieval service.

### Performance Targets
- p99 recommendation latency < 180 ms.
- Training refresh cadence: daily full, hourly incremental updates.
