#!/usr/bin/env python3
"""Module 3 artifact: simplified Dynamo-like key-value store.

Features:
- consistent hashing
- replication (N replicas)
- quorum writes/reads

Run:
  python3 module3_distributed_storage/kv_store.py
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Dict, List, Tuple


@dataclass
class VersionedValue:
    value: str
    version: int


class Node:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.data: Dict[str, VersionedValue] = {}
        self.up = True

    def put(self, key: str, value: str, version: int) -> None:
        existing = self.data.get(key)
        if existing is None or version >= existing.version:
            self.data[key] = VersionedValue(value=value, version=version)

    def get(self, key: str) -> VersionedValue | None:
        return self.data.get(key)


class ConsistentHashRing:
    def __init__(self, nodes: List[Node]) -> None:
        self.ring: List[Tuple[int, Node]] = sorted((self._h(n.node_id), n) for n in nodes)

    @staticmethod
    def _h(text: str) -> int:
        return int(hashlib.md5(text.encode()).hexdigest(), 16)

    def preference_list(self, key: str, replicas: int) -> List[Node]:
        kh = self._h(key)
        idx = 0
        for i, (token, _) in enumerate(self.ring):
            if token >= kh:
                idx = i
                break
        result: List[Node] = []
        i = idx
        while len(result) < replicas:
            node = self.ring[i % len(self.ring)][1]
            if node not in result:
                result.append(node)
            i += 1
        return result


class DynamoMini:
    def __init__(self, node_ids: List[str], n: int = 3, r: int = 2, w: int = 2) -> None:
        self.nodes = [Node(nid) for nid in node_ids]
        self.ring = ConsistentHashRing(self.nodes)
        self.n = n
        self.r = r
        self.w = w

    def set_node(self, node_id: str, up: bool) -> None:
        for node in self.nodes:
            if node.node_id == node_id:
                node.up = up
                print(f"node {node_id} {'UP' if up else 'DOWN'}")

    def put(self, key: str, value: str, version: int) -> bool:
        replicas = self.ring.preference_list(key, self.n)
        acks = 0
        for node in replicas:
            if node.up:
                node.put(key, value, version)
                acks += 1
        success = acks >= self.w
        print(f"PUT {key}={value}@v{version} -> acks={acks}/{self.n}, success={success}")
        return success

    def get(self, key: str) -> VersionedValue | None:
        replicas = self.ring.preference_list(key, self.n)
        responses: List[VersionedValue] = []
        for node in replicas:
            if node.up:
                v = node.get(key)
                if v:
                    responses.append(v)
            if len(responses) >= self.r:
                break
        if len(responses) < self.r:
            print(f"GET {key} failed quorum: got {len(responses)}<{self.r}")
            return None
        newest = max(responses, key=lambda x: x.version)
        print(f"GET {key} -> {newest.value}@v{newest.version} using {len(responses)} responses")
        return newest


def demo() -> None:
    store = DynamoMini(node_ids=["A", "B", "C", "D"], n=3, r=2, w=2)
    store.put("user:1", "alice", version=1)
    store.get("user:1")

    store.set_node("B", False)
    store.put("user:1", "alice-v2", version=2)
    store.get("user:1")

    store.set_node("C", False)
    store.get("user:1")


if __name__ == "__main__":
    demo()
