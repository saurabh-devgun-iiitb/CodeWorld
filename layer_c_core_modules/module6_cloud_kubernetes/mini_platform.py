#!/usr/bin/env python3
"""Module 6 executable: tiny Kubernetes-like platform simulator.

Models:
- scheduling to nodes with CPU capacity
- container lifecycle states
- autoscaling based on queue depth
- basic observability metrics
"""

from __future__ import annotations

from dataclasses import dataclass
from random import randint


@dataclass
class Node:
    name: str
    cpu_capacity: int
    cpu_used: int = 0


@dataclass
class Pod:
    name: str
    cpu_request: int
    state: str = "Pending"
    node: str | None = None


class MiniPlatform:
    def __init__(self) -> None:
        self.nodes = [Node("node-a", 8), Node("node-b", 8)]
        self.pods: list[Pod] = []

    def deploy(self, base_replicas: int) -> None:
        self.pods = [Pod(name=f"svc-{i}", cpu_request=2) for i in range(base_replicas)]

    def schedule(self) -> None:
        for pod in self.pods:
            if pod.state != "Pending":
                continue
            placed = False
            for node in self.nodes:
                if node.cpu_used + pod.cpu_request <= node.cpu_capacity:
                    node.cpu_used += pod.cpu_request
                    pod.state = "Running"
                    pod.node = node.name
                    placed = True
                    break
            if not placed:
                pod.state = "Unschedulable"

    def autoscale(self, queue_depth: int) -> None:
        target = max(2, min(8, queue_depth // 25 + 2))
        running_or_pending = len(self.pods)
        if target > running_or_pending:
            for i in range(running_or_pending, target):
                self.pods.append(Pod(name=f"svc-{i}", cpu_request=2))
        elif target < running_or_pending:
            self.pods = self.pods[:target]
            self._recompute_node_usage()

    def _recompute_node_usage(self) -> None:
        for node in self.nodes:
            node.cpu_used = 0
        for pod in self.pods:
            pod.state = "Pending"
            pod.node = None

    def metrics(self) -> dict[str, int]:
        running = sum(1 for p in self.pods if p.state == "Running")
        unsched = sum(1 for p in self.pods if p.state == "Unschedulable")
        return {"pods_total": len(self.pods), "pods_running": running, "pods_unschedulable": unsched}


def demo() -> None:
    platform = MiniPlatform()
    platform.deploy(base_replicas=2)

    for t in range(1, 16):
        queue_depth = randint(0, 180)
        platform.autoscale(queue_depth)
        platform.schedule()
        m = platform.metrics()
        print(f"tick={t:02d} queue={queue_depth:03d} metrics={m}")


if __name__ == "__main__":
    demo()
