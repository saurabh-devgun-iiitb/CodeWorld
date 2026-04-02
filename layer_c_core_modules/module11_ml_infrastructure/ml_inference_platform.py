"""Module 11: Multi-tenant ML inference platform model."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Dict


@dataclass
class TenantProfile:
    name: str
    rps: int
    avg_tokens: int


class InferencePlatform:
    def __init__(self) -> None:
        self.tenants = [
            TenantProfile("search", 300, 600),
            TenantProfile("support", 180, 1200),
            TenantProfile("ads", 520, 280),
        ]
        self.model_versions = {"ranker": ["1.2.0", "1.3.0"], "assistant": ["3.8.1", "3.9.0"]}
        self.max_rps_per_replica = 90

    def autoscaling_plan(self) -> Dict[str, int]:
        return {tenant.name: ceil(tenant.rps / self.max_rps_per_replica) for tenant in self.tenants}

    def batching_plan(self) -> Dict[str, int]:
        return {tenant.name: max(1, min(16, tenant.avg_tokens // 120)) for tenant in self.tenants}

    def rollout_strategy(self) -> Dict[str, str]:
        return {model: f"canary {versions[-1]} at 10% -> 50% -> 100%" for model, versions in self.model_versions.items()}


def main() -> None:
    platform = InferencePlatform()

    print("=== Multi-tenant ML Inference Platform ===")
    print("Autoscaling:")
    for tenant, replicas in platform.autoscaling_plan().items():
        print(f"- {tenant}: {replicas} replicas")

    print("\nModel versioning:")
    for model, versions in platform.model_versions.items():
        print(f"- {model}: active={versions[-1]}, previous={versions[-2]}")

    print("\nRequest batching:")
    for tenant, batch_size in platform.batching_plan().items():
        print(f"- {tenant}: batch_size={batch_size}")

    print("\nRollout strategy:")
    for model, rollout in platform.rollout_strategy().items():
        print(f"- {model}: {rollout}")

    print("\nOutcome: AI platform architecture understanding.")


if __name__ == "__main__":
    main()
