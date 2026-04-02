"""Module 9: Small observability stack simulation (metrics/logs/traces)."""

from __future__ import annotations

import random
from dataclasses import dataclass
from statistics import mean
from typing import List


@dataclass
class RequestSample:
    latency_ms: float
    status_code: int


class ObservabilityPipeline:
    def __init__(self, seed: int = 7) -> None:
        random.seed(seed)
        self.samples: List[RequestSample] = []

    def generate_traffic(self, n: int = 200) -> None:
        for idx in range(n):
            base = random.gauss(90, 20)
            if 120 <= idx < 150:  # injected latency spike window
                base += random.uniform(120, 280)
            latency = max(5, base)
            status = 500 if latency > 320 and random.random() < 0.5 else 200
            self.samples.append(RequestSample(latency, status))

    def export_metrics(self) -> dict:
        p95 = sorted(s.latency_ms for s in self.samples)[int(len(self.samples) * 0.95) - 1]
        error_rate = sum(1 for s in self.samples if s.status_code >= 500) / len(self.samples)
        return {"avg_latency_ms": round(mean(s.latency_ms for s in self.samples), 2), "p95_latency_ms": round(p95, 2), "error_rate": round(error_rate, 4)}

    def anomaly_detection(self, threshold_ms: float = 220.0) -> List[int]:
        return [i for i, s in enumerate(self.samples) if s.latency_ms > threshold_ms]


def main() -> None:
    pipe = ObservabilityPipeline()
    pipe.generate_traffic()

    metrics = pipe.export_metrics()
    anomalies = pipe.anomaly_detection()

    print("=== Observability Stack ===")
    print("service -> metrics exporter -> dashboard")
    print("\nMetrics:")
    for key, value in metrics.items():
        print(f"- {key}: {value}")

    print("\nLatency spikes detected:")
    print(f"- spike_count={len(anomalies)}")
    print(f"- sample_indexes(first 10)={anomalies[:10]}")

    bottleneck_hint = "database lock contention" if metrics["p95_latency_ms"] > 250 else "cpu pressure"
    print(f"\nLikely bottleneck signal: {bottleneck_hint}")
    print("Outcome: faster debugging of distributed systems behavior.")


if __name__ == "__main__":
    main()
