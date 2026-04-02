#!/usr/bin/env python3
"""Module 5 executable: simple cert rotation + auth policy simulation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Cert:
    version: int
    ttl_hours: int


class Service:
    def __init__(self, name: str) -> None:
        self.name = name
        self.cert = Cert(version=1, ttl_hours=24)

    def rotate_cert(self) -> None:
        self.cert = Cert(version=self.cert.version + 1, ttl_hours=24)


def is_allowed(src: str, dst: str) -> bool:
    allow = {("api", "payments"), ("payments", "ledger"), ("payments", "risk")}
    return (src, dst) in allow


def call(src: Service, dst: Service) -> None:
    if src.cert.ttl_hours <= 0 or dst.cert.ttl_hours <= 0:
        print(f"DENY {src.name}->{dst.name}: expired cert")
        return
    if not is_allowed(src.name, dst.name):
        print(f"DENY {src.name}->{dst.name}: policy")
        return
    print(f"ALLOW {src.name}->{dst.name}: mTLS certs v{src.cert.version}/v{dst.cert.version}")


def simulate() -> None:
    api = Service("api")
    payments = Service("payments")
    ledger = Service("ledger")

    for hour in range(1, 31):
        for svc in (api, payments, ledger):
            svc.cert.ttl_hours -= 1
            if svc.cert.ttl_hours <= 7:  # proactive rotation window
                svc.rotate_cert()
                print(f"[hour {hour}] rotated {svc.name} cert to v{svc.cert.version}")

        if hour in (1, 10, 20, 30):
            call(api, payments)
            call(api, ledger)
            call(payments, ledger)


if __name__ == "__main__":
    simulate()
