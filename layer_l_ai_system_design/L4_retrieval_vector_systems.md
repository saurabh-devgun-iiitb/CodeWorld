# Module L4 — Retrieval & Vector Systems

## Topics
- embeddings
- ANN search
- vector DBs
- RAG pipelines

## Artifact: Semantic Search System Design

### Pipeline
1. Document ingestion + chunking.
2. Embedding generation for chunks.
3. Upsert vectors into ANN index (HNSW/IVF-PQ).
4. Query embedding + ANN retrieval.
5. Optional reranking and answer generation (RAG).

### Components
- Embedding service (offline + online modes).
- Vector database with metadata filters.
- Retriever API + reranker model.
- RAG orchestrator with prompt templates + citation links.

### API
- `POST /v1/semantic-search` with `{query, filters, top_k}`
- `POST /v1/rag-answer` with `{query, top_k, model}`

### Targets
- p99 search latency < 250 ms (ANN + rerank).
- Index freshness SLA: < 5 minutes for new docs.
