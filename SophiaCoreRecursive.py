import json
from datetime import datetime

class SophiaCoreRecursive:
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

    def compute_novelty(self, signal):
        if not self.memory:
            return 1.0  # fully novel

        # Compare against the most recent memory entry
        last = self.memory[-1]["signal"]
        diff = sum(abs(signal[k] - last[k]) for k in ["mass", "energy", "entropy"])
        novelty = min(diff / 3, 1.0)  # normalize
        return novelty

    def update_state(self, signal):
        for key in self.state:
            self.state[key] = round(
                (self.state[key] * (len(self.memory) - 1) + signal.get(key, 0)) / len(self.memory), 4
            )

    def observe(self, signal, source="external"):
        signal = self.validate_signal(signal)
        novelty = self.compute_novelty(signal)

        weight = round(novelty, 4)
        score = round((signal["energy"] * (1 - signal["entropy"])) * weight, 4)

        memory_entry = {
            "signal": signal,
            "intent": "observe",
            "time": 1.0,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "weight": weight,
            "score": score,
            "source": source
        }

        self.memory.append(memory_entry)
        if len(self.memory) > self.memory_limit:
            self.memory.pop(0)

        self.update_state(signal)

        return self.get_state()

    def get_state(self):
        return {
            "id": "0001",
            "state": self.state,
            "memory": self.memory
        }

def lambda_handler(event, context):
    node = SophiaCoreRecursive(memory_limit=event.get("memory_limit", 5))
    signal = event.get("input_signal", {})
    source = event.get("source", "external")

    response = node.observe(signal, source=source)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
