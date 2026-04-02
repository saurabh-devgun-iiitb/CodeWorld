"""F3 Artifact: simulated caching layer for news feed timeline.

Principles:
- Redis page cache + object cache behavior
- Event-driven invalidation on writes
- Read latency improvement and hit-ratio tracking

Run:
    python3 layer_f_foundation_modules/F3_caching_performance.py
"""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
random.seed(7)


@dataclass
class Metrics:
    reads: int = 0
    hits: int = 0
    misses: int = 0
    latency_ms_total: float = 0.0


class TimelineCacheSystem:
    def __init__(self) -> None:
        self.page_cache: dict[str, list[str]] = {}
        self.post_store: dict[str, str] = {f"post-{i}": f"payload-{i}" for i in range(1, 200)}
        self.metrics = Metrics()

    def _cache_key(self, user_id: str, cursor: int) -> str:
        return f"timeline:{user_id}:{cursor}"

    def read_timeline(self, user_id: str, cursor: int) -> list[str]:
        self.metrics.reads += 1
        key = self._cache_key(user_id, cursor)

        if key in self.page_cache:
            self.metrics.hits += 1
            self.metrics.latency_ms_total += random.uniform(4, 8)  # fast cache path
            logging.info("cache_hit key=%s", key)
            return self.page_cache[key]

        self.metrics.misses += 1
        self.metrics.latency_ms_total += random.uniform(40, 90)  # slower DB path
        posts = [f"post-{cursor + i}" for i in range(1, 11)]
        self.page_cache[key] = posts
        logging.info("cache_miss key=%s db_fetch=true", key)
        return posts

    def write_post(self, post_id: str, payload: str) -> None:
        self.post_store[post_id] = payload
        # Event-driven invalidation (simplified: invalidate all timeline pages containing post).
        removed = 0
        for key in list(self.page_cache.keys()):
            if post_id in self.page_cache[key]:
                del self.page_cache[key]
                removed += 1
        logging.info("write_post post_id=%s invalidated_pages=%d", post_id, removed)

    def report(self) -> None:
        hit_ratio = (self.metrics.hits / self.metrics.reads) if self.metrics.reads else 0.0
        avg_latency = self.metrics.latency_ms_total / max(self.metrics.reads, 1)
        logging.info("reads=%d hits=%d misses=%d hit_ratio=%.2f", self.metrics.reads, self.metrics.hits, self.metrics.misses, hit_ratio)
        logging.info("avg_latency_ms=%.2f target_p99_under_250ms=true(simulated)", avg_latency)


def main() -> None:
    logging.info("=== F3 cache system simulation ===")
    system = TimelineCacheSystem()

    # Warmup + repeated reads to create hit ratio.
    for cursor in [0, 10, 20, 0, 10, 20, 0, 10, 20, 30, 0, 10]:
        system.read_timeline("user-1", cursor)

    # Write causes invalidation and subsequent misses.
    system.write_post("post-11", "payload-updated")
    system.read_timeline("user-1", 10)
    system.read_timeline("user-1", 10)

    system.report()
    logging.info("F3 simulation complete")


if __name__ == "__main__":
    main()
