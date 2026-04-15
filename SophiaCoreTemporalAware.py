
import json
from datetime import datetime

class SophiaCore:
    def __init__(self, memory_limit=5):
        self.state = {
            "energy": 0.0,
            "entropy": 0.0,
            "mass": 0.0,
            "time": 0.0
        }
        self.memory = []
        self.memory_limit = memory_limit

    def validate_signal(self, signal):
        if not isinstance(signal, dict):
            raise ValueError("Signal must be a dictionary.")
        for key in ["mass", "energy", "entropy"]:
            if key not in signal:
                raise ValueError(f"Missing key in signal: {key}")
        return signal

    def compute_delta(self, current, previous):
        return {
            key: round(current[key] - previous.get(key, 0.0), 4)
            for key in ["mass", "energy", "entropy"]
        }

    def observe(self, signal, source="external"):
        signal = self.validate_signal(signal)

        weight = 1.0
        base_score = signal["energy"] * (1 - signal["entropy"])
        last_signal = self.memory[-1]["signal"] if self.memory else {"mass": 0, "energy": 0, "entropy": 0}
        delta = self.compute_delta(signal, last_signal)
        temporal_score = sum(abs(v) for v in delta.values()) / 3

        memory_entry = {
            "signal": signal,
            "intent": "observe",
            "time": 1.0,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "weight": weight,
            "score": round(base_score, 4),
            "temporal_score": round(temporal_score, 4),
            "delta": delta,
            "source": source
        }

        self.memory.append(memory_entry)
        if len(self.memory) > self.memory_limit:
            self.memory.pop(0)

        return self.get_state()

    def get_state(self):
        return {
            "id": "0001",
            "state": self.state,
            "memory": self.memory
        }

def lambda_handler(event, context):
    node = SophiaCore(memory_limit=event.get("memory_limit", 5))
    signal = event.get("input_signal", {})
    source = event.get("source", "external")
    response = node.observe(signal, source=source)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
