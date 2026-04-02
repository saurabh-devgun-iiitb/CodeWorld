"""F2 Artifact: simulated data-modeling decisions for e-commerce and messaging.

Principles:
- SQL vs NoSQL selection by access pattern
- Indexing impact on query cost
- Denormalization tradeoff for reads

Run:
    python3 layer_f_foundation_modules/F2_data_modeling_storage.py
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


@dataclass
class QueryPlan:
    name: str
    base_rows_scanned: int
    has_index: bool

    def estimated_cost_ms(self) -> float:
        # Simple simulation: indexed queries scan ~2% of rows.
        scanned = int(self.base_rows_scanned * 0.02) if self.has_index else self.base_rows_scanned
        return round(scanned / 800.0, 2)


def ecommerce_simulation() -> None:
    logging.info("=== E-commerce model simulation ===")
    logging.info("Schema: users/orders/order_items/payments in SQL for ACID checkout")

    plans = [
        QueryPlan("list_user_orders", base_rows_scanned=120_000, has_index=True),
        QueryPlan("fetch_order_items", base_rows_scanned=900_000, has_index=True),
        QueryPlan("fraud_scan_recent_payments", base_rows_scanned=2_200_000, has_index=False),
    ]

    for plan in plans:
        logging.info(
            "query=%s indexed=%s est_cost_ms=%.2f",
            plan.name,
            plan.has_index,
            plan.estimated_cost_ms(),
        )

    logging.info("Denormalization: store product_snapshot in order_items for historical correctness")


def messaging_simulation() -> None:
    logging.info("=== Messaging model simulation ===")
    logging.info("Control plane in SQL (users/rooms/ACL), data plane in NoSQL (messages)")

    messages_per_room = {"room-hot": 1_500_000, "room-cold": 3_000}
    for room, count in messages_per_room.items():
        partition = room
        logging.info("room=%s partition_key=%s messages=%d", room, partition, count)

    logging.info("NoSQL read path: key=(room_id, timestamp) enables append + range scans")
    logging.info("Denormalization: unread_count precomputed per (user, room) to avoid expensive aggregations")


def main() -> None:
    ecommerce_simulation()
    messaging_simulation()
    logging.info("F2 simulation complete")


if __name__ == "__main__":
    main()
