#!/usr/bin/env python3
"""Module 4 prototype: event log + consumer lag/backpressure simulation."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from random import randint
from time import sleep


@dataclass
class Event:
    event_id: int
    payload: int


class MessageLog:
    def __init__(self) -> None:
        self.events: deque[Event] = deque()
        self.next_id = 0

    def append(self, payload: int) -> None:
        self.events.append(Event(self.next_id, payload))
        self.next_id += 1


class Consumer:
    def __init__(self) -> None:
        self.offset = 0
        self.processed = 0
        self.sum_payload = 0

    def poll(self, log: MessageLog, max_batch: int) -> int:
        processed_now = 0
        while self.offset < len(log.events) and processed_now < max_batch:
            ev = log.events[self.offset]
            self.sum_payload += ev.payload
            self.offset += 1
            self.processed += 1
            processed_now += 1
        return processed_now


def simulate(ticks: int = 40) -> None:
    log = MessageLog()
    consumer = Consumer()

    producer_rate = 30
    consumer_batch = 20

    for t in range(ticks):
        if t == 12:
            print("[experiment] Injecting slowdown")
            consumer_batch = 5
        if t == 22:
            print("[experiment] Recovering + autoscale")
            consumer_batch = 35

        produced = randint(max(1, producer_rate - 8), producer_rate + 8)
        for _ in range(produced):
            log.append(payload=1)

        consumed = consumer.poll(log, max_batch=consumer_batch)
        lag = len(log.events) - consumer.offset

        if lag > 200:
            producer_rate = max(10, producer_rate - 5)  # backpressure
        elif lag < 50:
            producer_rate = min(40, producer_rate + 2)

        print(
            f"tick={t:02d} produced={produced:02d} consumed={consumed:02d} "
            f"lag={lag:03d} producer_rate={producer_rate:02d}"
        )
        sleep(0.02)

    print(f"processed={consumer.processed}, aggregate_sum={consumer.sum_payload}, lag={len(log.events)-consumer.offset}")


if __name__ == "__main__":
    simulate()
