"""
Module 1 Artifact: Distributed Systems Failure Simulator

This simulator is intentionally educational (not production-accurate):
- It models asynchronous message delays using a time-ordered event queue.
- It supports node crashes (a node stops sending/receiving).
- It performs a simple leader election (highest alive node ID among reachable peers).
- It supports network partitions (links between groups are dropped).
- It demonstrates state divergence during partitioned operation.

Why this is useful for the syllabus:
- CAP theorem: during partition, we preserve availability in one partition but lose
  global consistency.
- Partial failures: node crashes and one-way communication failures are routine.
- Consensus basics: a designated leader coordinates writes for replication.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import heapq
import random
from typing import Callable, Dict, List, Set, Tuple


@dataclass
class Message:
    """Represents a message sent between nodes."""

    src: int
    dst: int
    kind: str
    payload: dict


@dataclass(order=True)
class ScheduledEvent:
    """Event in the simulation event queue (ordered by delivery time)."""

    delivery_time: int
    sequence: int
    action: Callable[[], None] = field(compare=False)


class Node:
    """
    Simulated cluster node.

    Local state:
    - `value`: simple integer register (our replicated state)
    - `term`: logical election term used for illustrative election progression
    - `leader_id`: node's current view of leader
    """

    def __init__(self, node_id: int) -> None:
        self.node_id = node_id
        self.alive = True
        self.value = 0
        self.term = 0
        self.leader_id: int | None = None

    def __repr__(self) -> str:
        status = "UP" if self.alive else "DOWN"
        return (
            f"Node(id={self.node_id}, status={status}, term={self.term}, "
            f"leader={self.leader_id}, value={self.value})"
        )


class ClusterSimulator:
    """Core simulation engine for a cluster of nodes."""

    def __init__(self, num_nodes: int, seed: int = 7) -> None:
        random.seed(seed)
        self.time = 0
        self.seq = 0
        self.events: List[ScheduledEvent] = []

        self.nodes: Dict[int, Node] = {i: Node(i) for i in range(1, num_nodes + 1)}

        # Connectivity matrix (u, v) -> True/False (whether traffic can pass).
        self.link_up: Dict[Tuple[int, int], bool] = {}
        for u in self.nodes:
            for v in self.nodes:
                if u != v:
                    self.link_up[(u, v)] = True

    # ---------- Event scheduling ----------

    def schedule(self, delay: int, action: Callable[[], None]) -> None:
        """Schedule an action for future simulated time."""
        self.seq += 1
        event = ScheduledEvent(self.time + delay, self.seq, action)
        heapq.heappush(self.events, event)

    def run(self, until_time: int | None = None) -> None:
        """Run scheduled events in chronological order."""
        while self.events:
            if until_time is not None and self.events[0].delivery_time > until_time:
                break
            event = heapq.heappop(self.events)
            self.time = event.delivery_time
            event.action()

    # ---------- Networking + failures ----------

    def set_link(self, src: int, dst: int, is_up: bool) -> None:
        self.link_up[(src, dst)] = is_up

    def can_deliver(self, src: int, dst: int) -> bool:
        return self.link_up.get((src, dst), False)

    def send(self, message: Message, min_delay: int = 1, max_delay: int = 4) -> None:
        """
        Send a message with random delay.

        Delivery is dropped if either endpoint is down or link is partitioned.
        """

        delay = random.randint(min_delay, max_delay)

        def deliver() -> None:
            src_node = self.nodes[message.src]
            dst_node = self.nodes[message.dst]

            if not src_node.alive:
                print(f"[t={self.time}] DROP {message.kind}: src {message.src} is down")
                return
            if not dst_node.alive:
                print(f"[t={self.time}] DROP {message.kind}: dst {message.dst} is down")
                return
            if not self.can_deliver(message.src, message.dst):
                print(
                    f"[t={self.time}] DROP {message.kind}: link {message.src}->{message.dst} partitioned"
                )
                return

            self.on_message(message)

        self.schedule(delay, deliver)

    def crash_node(self, node_id: int) -> None:
        self.nodes[node_id].alive = False
        print(f"[t={self.time}] NODE {node_id} crashed")

    def recover_node(self, node_id: int) -> None:
        self.nodes[node_id].alive = True
        print(f"[t={self.time}] NODE {node_id} recovered")

    def partition(self, group_a: Set[int], group_b: Set[int]) -> None:
        """Create bidirectional partition between two groups."""
        for a in group_a:
            for b in group_b:
                self.set_link(a, b, False)
                self.set_link(b, a, False)
        print(f"[t={self.time}] NETWORK PARTITION introduced: {group_a} | {group_b}")

    def heal_partition(self) -> None:
        for k in list(self.link_up.keys()):
            self.link_up[k] = True
        print(f"[t={self.time}] NETWORK PARTITION healed")

    # ---------- Leader election ----------

    def elect_leader(self, candidate_nodes: Set[int] | None = None) -> int | None:
        """
        Simple election rule:
        - Among alive candidate nodes, highest node ID becomes leader.

        This is a toy approximation of leader selection for educational use.
        """

        if candidate_nodes is None:
            candidate_nodes = set(self.nodes.keys())

        alive_candidates = [nid for nid in candidate_nodes if self.nodes[nid].alive]
        if not alive_candidates:
            print(f"[t={self.time}] ELECTION failed: no alive candidates")
            return None

        new_leader = max(alive_candidates)
        for nid, node in self.nodes.items():
            if nid in candidate_nodes:
                node.term += 1
                node.leader_id = new_leader

        print(
            f"[t={self.time}] LEADER ELECTED in scope {sorted(candidate_nodes)}: Node {new_leader}"
        )
        return new_leader

    # ---------- Replication behavior ----------

    def leader_write(self, leader_id: int, delta: int = 1) -> None:
        """Leader applies local write and asynchronously replicates to followers."""
        leader = self.nodes[leader_id]
        if not leader.alive:
            print(f"[t={self.time}] WRITE rejected: leader {leader_id} is down")
            return

        leader.value += delta
        new_value = leader.value
        print(f"[t={self.time}] LEADER {leader_id} write applied -> value={new_value}")

        for nid, node in self.nodes.items():
            if nid == leader_id:
                continue
            if not node.alive:
                continue

            msg = Message(
                src=leader_id,
                dst=nid,
                kind="REPLICATE",
                payload={"value": new_value, "term": leader.term},
            )
            self.send(msg)

    def on_message(self, msg: Message) -> None:
        """Handle incoming messages."""
        dst = self.nodes[msg.dst]

        if msg.kind == "REPLICATE":
            incoming_value = msg.payload["value"]

            # Simple last-writer-wins by max value in this toy model.
            if incoming_value > dst.value:
                old = dst.value
                dst.value = incoming_value
                print(
                    f"[t={self.time}] NODE {dst.node_id} applied replication: {old} -> {dst.value}"
                )
            else:
                print(
                    f"[t={self.time}] NODE {dst.node_id} ignored stale replication value={incoming_value}"
                )

    # ---------- Observability ----------

    def show_cluster_state(self, header: str) -> None:
        print(f"\n=== {header} @ t={self.time} ===")
        for nid in sorted(self.nodes):
            print(self.nodes[nid])

    def state_vector(self) -> Dict[int, int]:
        return {nid: node.value for nid, node in self.nodes.items()}


def run_partition_divergence_experiment() -> None:
    """
    Example experiment requested:
      In a simulated cluster:
      - introduce network partition
      - observe state divergence

    Steps:
    1) Start 5-node cluster, elect leader.
    2) Apply writes in healthy network.
    3) Crash one node to demonstrate partial failure.
    4) Partition network into {1,2,3} and {4,5}.
    5) Elect leaders per partition and write in majority partition.
    6) Observe state divergence.
    7) Heal partition and inspect final state.
    """

    sim = ClusterSimulator(num_nodes=5, seed=11)

    # Step 1: Initial full-cluster election
    global_leader = sim.elect_leader()
    sim.show_cluster_state("After initial leader election")

    # Step 2: Some normal writes and asynchronous replication delays
    if global_leader is not None:
        sim.leader_write(global_leader, delta=2)
        sim.leader_write(global_leader, delta=3)
    sim.run()
    sim.show_cluster_state("After normal operation writes")

    # Step 3: Crash one follower
    sim.crash_node(2)

    # Step 4: Partition the cluster
    group_a = {1, 2, 3}
    group_b = {4, 5}
    sim.partition(group_a, group_b)

    # Step 5: Leaders in each partition (toy behavior for demonstration)
    leader_a = sim.elect_leader(candidate_nodes=group_a)
    leader_b = sim.elect_leader(candidate_nodes=group_b)

    # Writes only in group A leader to intentionally induce divergence.
    if leader_a is not None:
        sim.leader_write(leader_a, delta=5)
        sim.leader_write(leader_a, delta=1)

    # Optional independent write in group B to show split-brain style drift.
    if leader_b is not None:
        sim.leader_write(leader_b, delta=2)

    sim.run()
    sim.show_cluster_state("During partition (expect divergence)")

    # Step 6: Explicit divergence observation
    vector = sim.state_vector()
    distinct_values = sorted(set(vector.values()))
    print(f"\n[t={sim.time}] State vector: {vector}")
    if len(distinct_values) > 1:
        print(
            f"[t={sim.time}] DIVERGENCE observed. Distinct replicated values: {distinct_values}"
        )
    else:
        print(f"[t={sim.time}] No divergence observed (all nodes equal).")

    # Step 7: Heal network and inspect (no anti-entropy implemented deliberately)
    sim.heal_partition()
    sim.run()
    sim.show_cluster_state("After healing partition")

    print(
        "\nNote: This educational simulator does not auto-reconcile all divergent states "
        "after healing. In real systems, repair mechanisms (anti-entropy, logs, quorum "
        "reads/writes, consensus protocols) address this."
    )


if __name__ == "__main__":
    run_partition_divergence_experiment()
