#!/usr/bin/env python3
"""Bonus prototype: idempotent request processing service.

Run:
  python3 module2_concurrency_transactions/idempotent_service.py
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from threading import Lock, Thread
from time import sleep
from typing import Any, Dict


@dataclass
class StoredResult:
    payload_hash: str
    response: Dict[str, Any]


class IdempotencyStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._data: Dict[str, StoredResult] = {}

    @staticmethod
    def _hash_payload(payload: Dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode()).hexdigest()

    def process(self, key: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload_hash = self._hash_payload(payload)

        with self._lock:
            existing = self._data.get(key)
            if existing:
                if existing.payload_hash != payload_hash:
                    return {
                        "status": 409,
                        "error": "Idempotency key reused with different payload",
                    }
                return {"status": 200, "result": existing.response, "replayed": True}

        # Simulated side effect outside lock (e.g., charge attempt).
        sleep(0.05)
        result = {
            "payment_id": f"pay_{payload['user_id']}_{payload['amount_cents']}",
            "captured_cents": payload["amount_cents"],
        }

        with self._lock:
            # Double-check for races.
            existing = self._data.get(key)
            if existing:
                if existing.payload_hash != payload_hash:
                    return {
                        "status": 409,
                        "error": "Idempotency key conflict after race",
                    }
                return {"status": 200, "result": existing.response, "replayed": True}

            self._data[key] = StoredResult(payload_hash=payload_hash, response=result)
            return {"status": 201, "result": result, "replayed": False}


def demo() -> None:
    store = IdempotencyStore()

    req_key = "tenantA:payments:create:abc123"
    payload = {"user_id": "u42", "amount_cents": 1999}

    def worker(name: str) -> None:
        res = store.process(req_key, payload)
        print(f"{name}: {res}")

    t1 = Thread(target=worker, args=("client-1",))
    t2 = Thread(target=worker, args=("client-2-retry",))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    conflict = store.process(req_key, {"user_id": "u42", "amount_cents": 2999})
    print(f"conflict-case: {conflict}")


if __name__ == "__main__":
    demo()
