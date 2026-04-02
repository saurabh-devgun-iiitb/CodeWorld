"""Module 8: Reliability engineering plan for a distributed checkout system."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SLO:
    name: str
    target: float
    window_days: int
    metric: str


class ReliabilityPlan:
    def __init__(self) -> None:
        self.slos = [
            SLO("api-availability", 99.95, 30, "successful_requests / total_requests"),
            SLO("p95-latency", 99.0, 30, "requests_under_250ms / total_requests"),
            SLO("order-durability", 99.99, 30, "durable_writes / write_attempts"),
        ]
        self.monitors = [
            "RED metrics: rate, errors, duration",
            "USE metrics on infra: utilization, saturation, errors",
            "trace sampling 10% baseline + tail-based sampling on high latency",
            "log-based alerts for payment-provider anomalies",
        ]
        self.failure_injection = [
            "Terminate 1/5 API pods during peak synthetic load",
            "Introduce 200ms DB latency for 15 minutes",
            "Drop 5% of inter-service traffic between API and payment service",
            "Simulate region failover in staging monthly",
        ]

    def error_budget_hours(self, availability_slo: float) -> float:
        total_hours = 30 * 24
        return total_hours * (1 - availability_slo / 100)

    def summarize(self) -> Dict[str, List[str]]:
        return {
            "slos": [f"{s.name}: {s.target}% over {s.window_days}d ({s.metric})" for s in self.slos],
            "monitoring": self.monitors,
            "failure_injection": self.failure_injection,
        }


def main() -> None:
    plan = ReliabilityPlan()
    summary = plan.summarize()

    print("=== Reliability Plan ===")
    print("SLO definitions:")
    for item in summary["slos"]:
        print(f"- {item}")

    primary_slo = plan.slos[0]
    budget = plan.error_budget_hours(primary_slo.target)
    print(f"\nError budget for {primary_slo.name}: {budget:.2f} hours / 30 days")

    print("\nMonitoring strategy:")
    for item in summary["monitoring"]:
        print(f"- {item}")

    print("\nFailure injection plan:")
    for item in summary["failure_injection"]:
        print(f"- {item}")

    print("\nOutcome: production-grade reliability decision-making.")


if __name__ == "__main__":
    main()
