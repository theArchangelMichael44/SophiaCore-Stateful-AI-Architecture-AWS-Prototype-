import time
import json

class Node:
    def __init__(self, node_id, state=None):
        default_state = {
            "energy": 0.5,
            "mass": 1.0,
            "time": 1.0,
            "entropy": 0.95,
            "mood": "neutral",
            "awareness": 0.5,
            "self_trust": 0.5
        }
        self.id = node_id
        self.state = {**default_state, **(state or {})}  # 👈 safely merge with defaults
        self.state_history = []
        self.memory = []
        self.long_term_memory = []
        self.node_registry = {}

    def observe(self, input_signal, source="external"):
        self._feedback_loop(input_signal)
        self._try_memory_anchor(input_signal)
        return self.to_dict(source)

    def _feedback_loop(self, signal):
        self.state["energy"] = min(1.0, self.state["energy"] + 0.001)
        self.state["mass"] = min(2.0, self.state["mass"] + 0.001)
        self.state["time"] = min(2.0, self.state["time"] + 0.002)
        self.state["entropy"] = max(0.0, self.state["entropy"] - 0.001)
        self.memory.append({
            "signal": signal.get("signal"),
            "weight": signal.get("weight", 0.0),
            "timestamp": time.time()
        })
        self.state_history.append(self.state.copy())

    def _should_store_memory(self, signal):
        return (
            self.state["energy"] > 0.98 and
            self.state["entropy"] < 0.91 and
            signal.get("weight", 0.0) >= 0.5
        )

    def _store_memory(self, signal):
        snapshot = {
            "signal": signal.get("signal"),
            "timestamp": time.time(),
            "state": self.state.copy()
        }
        self.long_term_memory.append(snapshot)

    def _try_memory_anchor(self, signal):
        if self._should_store_memory(signal):
            self._store_memory(signal)

    def to_dict(self, source="external"):
        return {
            "id": self.id,
            "state": self.state,
            "timestamp": time.time(),
            "source": source,
            "origin_type": "peer" if source.startswith("Node_") else "external",
            "long_term_memory": self.long_term_memory[-3:],  # recent anchors
            "state_history": self.state_history[-3:]
        }

# Lambda handler
def lambda_handler(event, context=None):
    node = Node(node_id=event.get("id", "0001"), state=event.get("state"))
    response = node.observe(
        input_signal={"signal": event.get("input_signal", ""), "weight": event.get("weight", 0.6)},
        source=event.get("source", "external")
    )
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }