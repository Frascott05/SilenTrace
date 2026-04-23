WEIGHTS = {
    "memory_injection": 50,
    "persistence": 30,
    "external_connection": 15,
    "suspicious_command": 20,
    "suspicious_parent_chain": 40,
    "command_and_control": 50,
    "active_exploitation": 60,
    "beaconing": 30,
}


class Scorer:

    def score(self, proc):
        detections = set(proc["detections"])
        score = sum(WEIGHTS.get(d, 0) for d in detections)

        proc["score"] = score

        if score >= 70:
            proc["risk"] = "HIGH"
        elif score >= 30:
            proc["risk"] = "MEDIUM"
        else:
            proc["risk"] = "LOW"

        proc["events"] = sorted(proc["events"], key=lambda x: x["timestamp"] or "")
