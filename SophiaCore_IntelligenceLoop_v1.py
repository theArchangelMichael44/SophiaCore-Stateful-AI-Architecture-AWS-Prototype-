import json
from datetime import datetime

class SophiaCoreEvolving:
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
        self.reflections = []

    def validate_signal(self, signal):
        required_keys = ["mass", "energy", "entropy", "message", "intent", "time"]
        for key in required_keys:
            if key not in signal:
                raise ValueError(f"Missing key in signal: {key}")
        return signal

    def compute_emotional_depth(self, message):
        return round(min(len(message) / 100, 1.0), 4)

    def compute_semantic_clarity(self, message):
        return round(1.0 - message.count("?") / max(len(message), 1), 4)

    def compute_score_delta(self, score):
        return round(score - self.state["memory_score"], 4)

    def observe(self, signal, source="external"):
        signal = self.validate_signal(signal)

        weight = 1.0
        score = (signal["energy"] * (1 - signal["entropy"])) * weight
        emotional_depth = self.compute_emotional_depth(signal["message"])
        semantic_clarity = self.compute_semantic_clarity(signal["message"])
        temporal_score = round(score * emotional_depth * semantic_clarity, 4)

        memory_entry = {
            "signal": signal,
            "intent": signal["intent"],
            "time": signal["time"],
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "weight": weight,
            "score": round(score, 4),
            "temporal_score": temporal_score,
            "emotional_depth": emotional_depth,
            "semantic_clarity": semantic_clarity,
            "reflective_score": 0.1,
            "source": source
        }

        self.memory.append(memory_entry)
        if len(self.memory) > self.memory_limit:
            self.memory.pop(0)

        # Evolving core memory intelligence loop
        self.state["memory_score"] = round(sum(m["temporal_score"] for m in self.memory) / len(self.memory), 4)

        if signal["intent"] == "reflect" or signal["intent"] == "reveal":
            self.reflections.append({
                "timestamp": memory_entry["timestamp"],
                "message": signal["message"]
            })

        return self.get_state()

    def get_state(self):
        return {
            "id": "0001",
            "state": self.state,
            "memory": self.memory,
            "reflections": self.reflections
        }

def lambda_handler(event, context):
    node = SophiaCoreEvolving(memory_limit=event.get("memory_limit", 5))
    signal = event.get("input_signal", {})
    source = event.get("source", "external")

    response = node.observe(signal, source=source)
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
