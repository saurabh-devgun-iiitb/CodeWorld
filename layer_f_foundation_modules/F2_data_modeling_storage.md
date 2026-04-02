# Module F2 — Data Modeling & Storage Basics

## Topics

- SQL vs NoSQL selection
- Schema design fundamentals
- Indexing strategy
- Denormalization tradeoffs

## Artifact 1: E-commerce Schema Design

### SQL Core Entities
- `users`, `products`, `inventory`, `orders`, `order_items`, `payments`

### Key Design Choices
- Normalize transactional entities (`orders`, `payments`).
- Denormalize product snapshot fields into `order_items` for audit safety.
- Composite indexes:
  - `orders(user_id, created_at desc)`
  - `order_items(order_id, product_id)`

### Storage Notes
- SQL for transactional consistency.
- Optional document store for product search/catalog facets.

## Artifact 2: Messaging System Schema Design

### Hybrid Model
- SQL: accounts, room metadata, ACLs.
- NoSQL wide-column/document: messages by `(room_id, message_ts)`.

### Indexing
- Partition/shard key by room.
- Secondary index for sender-based moderation queries.

### Denormalization
- Store sender display name/avatar snapshot in message envelope.
- Maintain unread counters in precomputed user-room state table.


## Runnable Artifact

- Script: `F2_data_modeling_storage.py`
- Run: `python3 layer_f_foundation_modules/F2_data_modeling_storage.py`
