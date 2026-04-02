"""F1 Artifact: simulated API request lifecycle (URL shortener + chat service).

Principles demonstrated:
- Client -> LB -> Service -> DB request flow
- Idempotency handling for retries
- Cursor pagination
- Rate limiting

Run:
    python3 layer_f_foundation_modules/F1_api_request_lifecycle.py
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


@dataclass
class Request:
    request_id: str
    user_id: str
    path: str
    method: str
    idempotency_key: str | None = None


class TokenBucketLimiter:
    """Simple per-user token bucket for simulation."""

    def __init__(self, capacity: int, refill_per_second: float) -> None:
        self.capacity = capacity
        self.refill = refill_per_second
        self.tokens: dict[str, float] = defaultdict(lambda: float(capacity))
        self.last: dict[str, float] = defaultdict(time.time)

    def allow(self, user_id: str) -> bool:
        now = time.time()
        elapsed = now - self.last[user_id]
        self.last[user_id] = now
        self.tokens[user_id] = min(self.capacity, self.tokens[user_id] + elapsed * self.refill)
        if self.tokens[user_id] >= 1:
            self.tokens[user_id] -= 1
            return True
        return False


class UrlShortenerService:
    """Simulates DB-backed shortener with idempotency table."""

    def __init__(self) -> None:
        self.url_db: dict[str, str] = {}
        self.idempotency_store: dict[str, dict] = {}
        self.seq = 1000

    def create(self, req: Request, long_url: str) -> dict:
        if req.idempotency_key and req.idempotency_key in self.idempotency_store:
            logging.info("[service] idempotent replay request_id=%s", req.request_id)
            return self.idempotency_store[req.idempotency_key]

        self.seq += 1
        short_code = f"u{self.seq}"
        self.url_db[short_code] = long_url
        response = {"short_code": short_code, "long_url": long_url}
        if req.idempotency_key:
            self.idempotency_store[req.idempotency_key] = response
        logging.info("[db] inserted mapping short_code=%s", short_code)
        return response


class ChatService:
    """Simulates chat writes/reads with dedupe + cursor pagination."""

    def __init__(self) -> None:
        self.messages: dict[str, deque[dict]] = defaultdict(deque)
        self.client_message_ids: set[str] = set()

    def send_message(self, room_id: str, sender: str, client_message_id: str, text: str) -> dict:
        if client_message_id in self.client_message_ids:
            logging.info("[chat] duplicate client_message_id=%s ignored", client_message_id)
            return {"status": "duplicate"}

        self.client_message_ids.add(client_message_id)
        msg = {
            "msg_id": f"m{len(self.messages[room_id]) + 1}",
            "sender": sender,
            "text": text,
        }
        self.messages[room_id].append(msg)
        return {"status": "accepted", "message": msg}

    def list_messages(self, room_id: str, cursor: int, limit: int = 3) -> dict:
        rows = list(self.messages[room_id])
        page = rows[cursor : cursor + limit]
        next_cursor = cursor + limit if (cursor + limit) < len(rows) else None
        return {"items": page, "next_cursor": next_cursor}


def simulate_request_flow(req: Request) -> None:
    logging.info("[client] -> [lb] request_id=%s %s %s", req.request_id, req.method, req.path)
    logging.info("[lb] -> [service] routed to application shard")


def main() -> None:
    logging.info("=== F1 lifecycle simulation ===")
    limiter = TokenBucketLimiter(capacity=3, refill_per_second=1.0)
    shortener = UrlShortenerService()
    chat = ChatService()

    req = Request("r-1", "alice", "/v1/short-urls", "POST", idempotency_key="idem-11")
    simulate_request_flow(req)
    if limiter.allow(req.user_id):
        logging.info("[gateway] rate-limit passed")
        logging.info("response=%s", shortener.create(req, "https://example.com/docs/system-design"))

    # Retry same request with same idempotency key.
    retry = Request("r-2", "alice", "/v1/short-urls", "POST", idempotency_key="idem-11")
    simulate_request_flow(retry)
    logging.info("response=%s", shortener.create(retry, "https://example.com/docs/system-design"))

    # Chat flow: send and paginate.
    for i in range(1, 7):
        cid = f"cmsg-{i if i != 4 else 3}"  # deliberate duplicate when i=4
        result = chat.send_message("room-42", "alice", cid, f"hello-{i}")
        logging.info("chat_send[%d]=%s", i, result["status"])

    page1 = chat.list_messages("room-42", cursor=0, limit=3)
    page2 = chat.list_messages("room-42", cursor=page1["next_cursor"] or 0, limit=3)
    logging.info("page1_count=%d next=%s", len(page1["items"]), page1["next_cursor"])
    logging.info("page2_count=%d next=%s", len(page2["items"]), page2["next_cursor"])

    # Rate-limit demonstration: consume quickly
    outcomes = [limiter.allow("bob") for _ in range(5)]
    logging.info("rate_limit_outcomes_for_bob=%s", outcomes)
    logging.info("F1 simulation complete")


if __name__ == "__main__":
    main()
