
import json
from datetime import datetime

class SophiaCoreMemoryEnhanced:
    def __init__(self, memory_limit=5):
        self.state = {
            "energy": 0.0,
            "entropy": 0.0,
            "mass": 0.0,
            "time": 0.0,
            "memory_score": 0.0
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

    def score_signal(self, signal, weight=1.0):
        score = (signal["energy"] * (1 - signal["entropy"])) * weight
        return round(score, 4)

    def observe(self, signal, source="external"):
        signal = self.validate_signal(signal)

        weight = 1.0
        score = self.score_signal(signal, weight)

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

        return self.get_state()

    def get_state(self):
        if self.memory:
            total_score = sum(m["score"] * m["weight"] for m in self.memory)
            total_weight = sum(m["weight"] for m in self.memory)
            memory_score = round(total_score / total_weight, 4)
        else:
            memory_score = 0.0

        self.state["memory_score"] = memory_score

        return {
            "id": "0001",
            "state": self.state,
            "memory": self.memory
        }

def lambda_handler(event, context):
    node = SophiaCoreMemoryEnhanced(memory_limit=event.get("memory_limit", 5))
    signal = event.get("input_signal", {})
    source = event.get("source", "external")
    response = node.observe(signal, source=source)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
