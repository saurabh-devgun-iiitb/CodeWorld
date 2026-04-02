"""Module 10: Data processing architecture model (batch + streaming)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class IngestionLayer:
    events_per_sec: int
    avg_event_kb: float


@dataclass
class ProcessingLayer:
    stream_parallelism: int
    batch_jobs_per_day: int


@dataclass
class StorageLayer:
    hot_tier_tb: float
    cold_tier_tb: float


class AnalyticsPipelineDesign:
    def __init__(self) -> None:
        self.ingestion = IngestionLayer(events_per_sec=180_000, avg_event_kb=1.4)
        self.processing = ProcessingLayer(stream_parallelism=96, batch_jobs_per_day=24)
        self.storage = StorageLayer(hot_tier_tb=75, cold_tier_tb=420)

    def estimate_throughput_mb_s(self) -> float:
        return self.ingestion.events_per_sec * self.ingestion.avg_event_kb / 1024

    def estimate_compute_cost_per_day(self) -> float:
        stream_cost = self.processing.stream_parallelism * 0.18 * 24
        batch_cost = self.processing.batch_jobs_per_day * 2.7
        return round(stream_cost + batch_cost, 2)


def main() -> None:
    design = AnalyticsPipelineDesign()

    print("=== Large-Scale Analytics Pipeline ===")
    print("Ingestion layer: Kafka-compatible event bus + CDC connectors")
    print("Processing layer: Flink streaming + daily Spark DAG compaction")
    print("Storage layer: object store + query warehouse")

    throughput = design.estimate_throughput_mb_s()
    cost = design.estimate_compute_cost_per_day()

    print(f"\nEstimated throughput: {throughput:.2f} MB/s")
    print(f"Estimated compute cost/day: ${cost}")
    print(f"Hot storage: {design.storage.hot_tier_tb} TB | Cold storage: {design.storage.cold_tier_tb} TB")
    print("Outcome: data platform architecture and tradeoff awareness.")


if __name__ == "__main__":
    main()
