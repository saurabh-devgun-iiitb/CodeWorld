"""F4 Artifact: simulated stateful vs stateless session architecture.

Principles:
- Stateless access token validation at service nodes
- Stateful refresh/session metadata in shared store
- Global logout propagation across distributed nodes

Run:
    python3 layer_f_foundation_modules/F4_stateful_vs_stateless.py
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


@dataclass
class SessionRecord:
    user_id: str
    device_id: str
    refresh_token: str
    issued_at: int
    revoked: bool = False


class SessionStore:
    """Shared distributed state (e.g., Redis + durable backup)."""

    def __init__(self) -> None:
        self.records: dict[str, SessionRecord] = {}
        self.revoked_users: set[str] = set()

    def create(self, user_id: str, device_id: str) -> SessionRecord:
        refresh = f"r-{user_id}-{device_id}-{int(time.time())}"
        record = SessionRecord(user_id=user_id, device_id=device_id, refresh_token=refresh, issued_at=int(time.time()))
        self.records[refresh] = record
        return record

    def revoke(self, refresh_token: str) -> None:
        if refresh_token in self.records:
            self.records[refresh_token].revoked = True
            self.revoked_users.add(self.records[refresh_token].user_id)


class ServiceNode:
    """Stateless API node validating short-lived access tokens."""

    def __init__(self, name: str, store: SessionStore) -> None:
        self.name = name
        self.store = store

    def validate_access_token(self, access_token: str) -> bool:
        # Token format for demo: a-{user_id}-{epoch}
        user_id = access_token.split("-")[1]
        valid = user_id not in self.store.revoked_users
        logging.info("node=%s validate user=%s valid=%s", self.name, user_id, valid)
        return valid


def main() -> None:
    logging.info("=== F4 session architecture simulation ===")
    store = SessionStore()
    node_a = ServiceNode("api-a", store)
    node_b = ServiceNode("api-b", store)

    # Login flow: token can hit any node (stateless).
    session = store.create("u1", "mobile")
    access_token = f"a-u1-{int(time.time())}"
    logging.info("issued refresh=%s access=%s", session.refresh_token, access_token)

    _ = node_a.validate_access_token(access_token)
    _ = node_b.validate_access_token(access_token)

    # Global logout revokes centrally; all nodes observe distributed state.
    store.revoke(session.refresh_token)
    logging.info("global_logout refresh=%s propagated", session.refresh_token)

    _ = node_a.validate_access_token(access_token)
    _ = node_b.validate_access_token(access_token)

    logging.info("F4 simulation complete")


if __name__ == "__main__":
    main()
